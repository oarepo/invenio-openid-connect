# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET.
#
# OArepo OpenID Connect is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Flask extension for OArepo OpenID Connect."""

from __future__ import absolute_import, print_function

from . import config


class OArepoOpenIDConnect(object):
    """OArepo OpenID Connect extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        app.extensions['oarepo-openid-connect'] = self

    def init_config(self, app):
        """Initialize configuration.

        Override configuration variables with the values in this package.
        """
        pass
