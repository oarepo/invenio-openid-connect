# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET z.s.p.o..
#
# OARepo is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from flask import Blueprint, jsonify, session
from flask_babelex import refresh, get_locale
from flask_login import current_user
import humps

blueprint = Blueprint(
    'invenio_openid_connect',
    __name__,
    url_prefix='/oauth')


@blueprint.route('/state/')
def state():
    refresh()
    if current_user.is_anonymous:
        resp = {
            'loggedIn': False,
            'user': None,
            'userInfo': None,
            'language': get_locale().language
        }
    else:
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
            'userInfo': humps.camelize(session.get('user_info', None).to_dict()),
            'language': get_locale().language
        }

    return jsonify(resp)
