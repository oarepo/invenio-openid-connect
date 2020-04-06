# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET z.s.p.o..
#
# OARepo is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from flask import Blueprint
from invenio_oauthclient.views.client import login as _login, \
    authorized as _authorized, \
    signup as _signup, \
    disconnect as _disconnect


blueprint = Blueprint(
    'invenio_openid_connect',
    __name__,
    url_prefix='/openid')


@blueprint.route('/login/<remote_app>/')
def login(remote_app):
    """Send user to remote application for authentication."""
    return _login(remote_app)


@blueprint.route('/authorized/<remote_app>/')
def authorized(remote_app=None):
    """Authorized handler callback."""
    return _authorized(remote_app)

@blueprint.route('/signup/<remote_app>/', methods=['GET', 'POST'])
def signup(remote_app):
    """Extra signup step."""
    return _signup(remote_app)


@blueprint.route('/disconnect/<remote_app>/')
def disconnect(remote_app):
    """Disconnect user from remote application."""
    return _disconnect(remote_app)
