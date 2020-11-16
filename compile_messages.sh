#!/bin/bash

pybabel extract -F babel.cfg -o invenio_openid_connect/translations/messages.pot invenio_openid_connect
pybabel update -d invenio_openid_connect/translations -i invenio_openid_connect/translations/messages.pot -l cs
pybabel update -d invenio_openid_connect/translations -i invenio_openid_connect/translations/messages.pot -l en
pybabel compile -d invenio_openid_connect/translations

