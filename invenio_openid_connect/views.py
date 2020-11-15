# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET z.s.p.o..
#
# OARepo is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""Definition of state view."""

import humps
from flask import Blueprint, jsonify, session
from flask_babelex import get_locale, refresh
from flask_login import current_user

blueprint = Blueprint(
    'invenio_openid_connect',
    __name__,
    url_prefix='/oauth')


@blueprint.route('/state/')
def state():
    """
    State view.

    :return: json with serialized information about the current user
    """
    refresh()
    if current_user.is_anonymous:
        resp = {
            'loggedIn': False,
            'user': None,
            'userInfo': None,
            'language': get_locale().language
        }
    else:
        ui = session.get('user_info', None)
        if ui and not isinstance(ui, dict):
            ui = ui.to_dict()
        resp = {
            'loggedIn': True,
            'user': {
                'id': current_user.id,
                'email': current_user.email,
                'roles': [
                    {
                        'id': x.name,
                        'label': x.description
                    } for x in current_user.roles
                ]
            },
            'userInfo': humps.camelize(ui) if ui else {},
            'language': get_locale().language
        }

    return jsonify(resp)
