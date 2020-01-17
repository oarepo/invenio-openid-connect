# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET z.s.p.o..
#
# OARepo is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Helper functions for OArepo OpenID Connect Auth backend."""
from flask_oauthlib.client import OAuthException, OAuthResponse


def get_dict_from_response(response: OAuthResponse) -> dict:
    """Check for errors in the response and return the resulting dict.

    :param response: The OAuth response.
    :returns: Response data dict
    """
    if getattr(response, '_resp') and response._resp.code > 400:
        raise OAuthException(
            'OpenID Remote Application failed to parse response',
            None, response
        )

    return response.data
