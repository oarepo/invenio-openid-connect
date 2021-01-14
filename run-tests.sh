#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET.
#
# Invenio OpenID Connect is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

pydocstyle invenio_openid_connect tests && \
isort -c invenio_openid_connect tests && \
check-manifest --ignore ".travis-*" && \
python setup.py test
