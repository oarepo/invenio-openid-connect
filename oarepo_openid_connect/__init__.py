# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET.
#
# OArepo OpenID Connect is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""OArepo OpenID Connect Auth Backend"""

from __future__ import absolute_import, print_function

from .ext import OArepoOpenIDConnect
from .version import __version__
from .remote import OarepoAuthOpenIdRemote

__all__ = ('__version__', 'OArepoOpenIDConnect', 'OarepoAuthOpenIdRemote')
