# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET.
#
# Invenio OpenID Connect is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Invenio OpenID Connect Auth Backend."""

from __future__ import absolute_import, print_function

from .ext import InvenioOpenIDConnect
from .remote import InvenioAuthOpenIdRemote
from .version import __version__

__all__ = ('__version__', 'InvenioOpenIDConnect', 'InvenioAuthOpenIdRemote')
