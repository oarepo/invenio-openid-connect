# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET z.s.p.o..
#
# OARepo is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Remote application for enabling sign in/up with OpenID Connect."""
import traceback
from typing import Optional
from urllib.parse import urljoin

from flask import current_app, redirect, session, url_for
from flask_login import current_user
from flask_oauthlib.client import OAuthException, OAuthRemoteApp
from invenio_db import db
from invenio_oauthclient.models import RemoteAccount
from invenio_oauthclient.utils import oauth_link_external_id, \
    oauth_unlink_external_id
from werkzeug.local import LocalProxy

from .utils import get_dict_from_response


class LazyOAuthRemoteApp(OAuthRemoteApp):
    """OAuth remote app that can have lazy properties."""

    def __init__(self, *args, **kwargs):
        """constructor."""
        super().__init__(*args, **{
            **kwargs,
            'app_key': 'dummy test'
        })
        self.app_key = None

    def _get_property(self, key, default=False):
        ret = super()._get_property(key, default)
        if isinstance(ret, LocalProxy):
            ret = ret._get_current_object()
        return ret


class InvenioAuthOpenIdRemote(object):
    """Invenio OpenID Connect Abstract Remote App."""

    CONFIG_OPENID = 'OPENIDC_CONFIG'
    """Config key for openid."""

    CONFIG_OPENID_CREDENTIALS = 'OPENIDC_CREDENTIALS'
    """Config key for openid credentials."""

    name = 'OpenIDC'
    description = 'OpenID Connect'
    icon = ''
    userinfo_cls = None

    def remote_app(self) -> dict:
        """Configures and returns remote app."""
        return dict(
            title=self.name,
            description=self.description,
            icon=self.icon,
            authorized_handler=self.handle_authorized,
            disconnect_handler=self.handle_disconnect,
            signup_handler=dict(
                info=self.account_info,
                setup=self.account_setup,
                view=self.handle_signup,
            ),
            remote_app=LazyOAuthRemoteApp,
            params=dict(
                request_token_params={
                    # 'scope': LocalProxy(lambda: self.get_scope()),
                    # 'show_login': 'true'
                },
                base_url=LocalProxy(lambda: self.get_base_url()),
                request_token_url=LocalProxy(lambda: self.get_request_token_url()),
                access_token_url=LocalProxy(lambda: self.get_access_token_url()),
                access_token_method=LocalProxy(lambda: self.get_access_token_method()),
                authorize_url=LocalProxy(lambda: self.get_authorize_url()),
                content_type='application/json',
                signature_method=LocalProxy(lambda: self.get_signature_method()),
                consumer_key=LocalProxy(lambda: self.get_consumer_key()),
                consumer_secret=LocalProxy(lambda: self.get_consumer_secret())
            )
        )

    def get_base_url(self) -> str:
        """Return base URL for an OpenIDC provider."""
        return current_app.config[self.CONFIG_OPENID]['base_url']

    def get_request_token_url(self) -> Optional[str]:
        """Return request token endpoint URL for an OpenIDC provider."""
        url = current_app.config[self.CONFIG_OPENID].get('request_token_url', None)
        if not url:
            return None
        return urljoin(self.get_base_url(), url)

    def get_access_token_url(self) -> str:
        """Return access token endpoint for an OpenIDC provider."""
        return urljoin(self.get_base_url(),
                       current_app.config[self.CONFIG_OPENID].get('access_token_url', 'token'))

    def get_access_token_method(self) -> str:
        """Return method of obtaining an access token."""
        return current_app.config[self.CONFIG_OPENID].get('access_token_method', 'POST')

    def get_authorize_url(self) -> str:
        """Return authorize endpoint for an OpenIDC provider."""
        return urljoin(self.get_base_url(),
                       current_app.config[self.CONFIG_OPENID].get('authorize_url', 'authorize'))

    def get_userinfo_url(self) -> str:
        """Return remote user info endpoint."""
        return urljoin(self.get_base_url(),
                       current_app.config[self.CONFIG_OPENID].get('userinfo_url', 'userinfo'))

    def get_scope(self):
        """Return OpenID Connect client scopes."""
        return current_app.config[self.CONFIG_OPENID].get('scope', 'openid email profile')

    def get_signature_method(self):
        """Return oauth signature method."""
        return current_app.config[self.CONFIG_OPENID].get('signature_method', 'HMAC-SHA1')

    def get_consumer_key(self):
        """Return oauth consumer key."""
        return current_app.config[self.CONFIG_OPENID]['consumer_key']

    def get_consumer_secret(self):
        """Return oauth consumer key."""
        return current_app.config[self.CONFIG_OPENID]['consumer_secret']

    def get_userinfo(self, remote):
        """Retrieve external user information from the remote userinfo endpoint.

        :param remote: The remote application.
        :returns: A dictionary with the external user information
        """
        if not self.userinfo_cls:
            raise AttributeError('{}: userinfo_cls must be set'.format(self.name))

        cached_user_info = session.get('user_info')
        if cached_user_info:
            return cached_user_info

        response = remote.get(self.get_userinfo_url())
        user_info = self.userinfo_cls(get_dict_from_response(response))
        session['user_info'] = user_info

        return user_info

    def get_user_id(self, remote, email: str = None) -> str:
        """Determine ID for a given user/email.

        :param id_claim: Claim name containing user ID
        :param remote: The remote application.
        :param email: (optional) User e-mail address
        :returns: User ID
        """
        user_id = self.get_userinfo(remote).sub
        if not user_id:
            raise OAuthException(
                'User {} is missing *sub* attribute for '
                '{} Remote Application'.format(email, self.name),
                None, None
            )
        return user_id

    def account_info(self, remote, resp) -> dict:
        """Retrieve remote account information used to find local user.

        :param remote: The remote application.
        :param resp: The response.
        :returns: A dictionary with the user information.
        """
        user_info = self.get_userinfo(remote)
        return dict(
            user=dict(
                email=user_info.email,
                profile=dict(
                    username=user_info.username,
                    full_name=user_info.name
                ),
            ),
            external_id=self.get_user_id(remote, email=user_info.email),
            external_method=self.name,
            active=True
        )

    def account_setup(self, remote, token, resp):
        """Perform additional setup after user have been logged in.

        :param remote: The remote application.
        :param token: The token value.
        :param resp: The response.
        """
        user_info = self.get_userinfo(remote)
        user_id = self.get_user_id(remote, email=user_info.email)

        with db.session.begin_nested():
            # Put userinfo in extra_data.
            extra_data = user_info.__dict__
            extra_data['external_id'] = user_id
            extra_data['external_method'] = self.name
            token.remote_account.extra_data = extra_data
            user = token.remote_account.user

            # Create user <-> external id link.
            oauth_link_external_id(user, {'id': user_id, 'method': self.name})

    def handle_authorized(self, resp, remote, *args, **kwargs):
        """Callback for handling user authorization."""
        from invenio_oauthclient.handlers import authorized_signup_handler
        return authorized_signup_handler(resp, remote, *args, **kwargs)

    def handle_signup(self, remote, *args, **kwargs):
        """Callback for handling user signup."""
        from invenio_oauthclient.handlers import signup_handler
        return signup_handler(remote, *args, **kwargs)

    def handle_disconnect(self, remote, *args, **kwargs):
        """Handle unlinking of remote account.

        :param remote: The remote application.
        """
        if not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()

        account = RemoteAccount.get(user_id=current_user.get_id(),
                                    client_id=remote.consumer_key)
        sub = account.extra_data.get('sub')

        if sub:
            oauth_unlink_external_id({'id': sub, 'method': self.name})
        if account:
            with db.session.begin_nested():
                account.delete()

        return redirect(url_for('invenio_oauthclient_settings.index'))
