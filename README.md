# Invenio OpenID Connect

[![image][]][1]
[![image][2]][3] <!-- [![image][4]][5] -->
[![image][6]][7]


## Installation

Invenio OpenID Connect is on PyPI so all you need is:

``` console
$ pip install invenio-openid-connect
```

## Configuration

At first add this client to your openid server and get ``key`` and ``secret``.
Do not forget to set the allowed redirect url to:

``https://localhost:5000/api/oauth/authorized/openid/``

Then configure the backend handler in invenio.cfg

```python
from invenio_openid_connect import InvenioAuthOpenIdRemote

OPENIDC_CONFIG = dict(
    base_url='https://<openid-server>/openid/',
    consumer_key='<key from openid server>',
    consumer_secret='<secret from openid server>',
    # request_token_url = base_url
    # access_token_url = f'${base_url}/token'
    # access_token_method = 'POST'
    # authorize_url = f'${base_url}/authorize'
    # userinfo_url = f'${base_url}/userinfo'
    # scope = 'openid email profile'
    # signature_method = 'HMAC-SHA1'
    # # fields that will be used as a source of username (in this order, first field with value wins)
    # username_fields = ['username', 'preferred_username', 'sub', 'email']
)

OAUTHCLIENT_REST_REMOTE_APPS = dict(
    # the class from above, the auth method will be called "openid"
    openid=InvenioAuthOpenIdRemote().remote_app(),
)
```

Note that the redirect uri above ends with ``openid`` - this is the same key as in ``OAUTHCLIENT_REST_REMOTE_APPS``.

## Usage

After local configuration and allowing access at your , head in your browser to ``https://localhost:5000/api/oauth/login/openid?next=/api/oauth/state``
(``openid`` is the key in ``OAUTHCLIENT_REST_REMOTE_APPS``). You should log in with your openid provider and be redirected to state
API which accesses your userinfo data.

### OpenID backend

To extend the functionality of the backend (for example, to add a custom UserInfo class) you might want to write your own backend.

```python
from invenio_openid_connect import InvenioAuthOpenIdRemote

class CISLoginAuthRemote(InvenioAuthOpenIdRemote):
    # the name of the config settings in invenio.cfg . Default is OPENIDC_CONFIG
    CONFIG_OPENID = 'CIS_LOGIN_CONFIG'

    # human stuff
    name = 'CIS Login Server'
    description = 'Login server at CIS UCT Prague'
    icon = ''

    # userinfo class
    userinfo_cls = CISLoginUserInfoClass
```

Note that if your userinfo class does not inherit from ``dict`` it must implement ``to_dict`` method that is used
by the ``state`` endpoint.

```python
class CISLoginUserInfoClass:
    sub: str = None
    name: str = None
    preferred_username: str = None
    given_name: str = None
    family_name: str = None
    zoneinfo: str = None
    locale: str = None
    email: str = None
    roles: dict = {}

    def __init__(self, userinfo: dict):
        for k, v in userinfo.items():
            setattr(self, k, v)
        self.roles = userinfo.get('http://cis.vscht.cz/openid#roles', {})

    def to_dict(self):
        return self.__dict__

    @property
    def username(self):
        if self.preferred_username:
            return self.preferred_username
        elif self.email:
            return self.email
        return self.sub
```

Then configure the remote as above.


  [image]: https://img.shields.io/github/license/oarepo/invenio-openid-connect.svg
  [1]: https://github.com/oarepo/invenio-openid-connect/blob/master/LICENSE
  [2]: https://img.shields.io/travis/oarepo/invenio-openid-connect.svg
  [3]: https://travis-ci.com/oarepo/invenio-openid-connect
  [4]: https://img.shields.io/coveralls/oarepo/oarepo-openid-connect.svg
  [5]: https://coveralls.io/r/oarepo/invenio-openid-connect
  [6]: https://img.shields.io/pypi/v/invenio-openid-connect.svg
  [7]: https://pypi.org/pypi/invenio-openid-connect
