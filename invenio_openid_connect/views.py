# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET z.s.p.o..
#
# OARepo is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from flask import Blueprint
from invenio_oauthclient.views.client import login, authorized


blueprint = Blueprint(
    'invenio_openid_connect',
    __name__,
    url_prefix='/openid')


@blueprint.route('/login/<remote_app>/')
def openid_login(remote_app):
    return login(remote_app)


@blueprint.route('/authorized/<remote_app>/')
def openid_authorized(remote_app=None):
    return authorized(remote_app)
