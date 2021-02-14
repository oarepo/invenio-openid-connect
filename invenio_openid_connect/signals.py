from blinker import Namespace

_signals = Namespace()

prepare_state_view_data = _signals.signal('prepare-state-view-data')
"""
Signal sent just before state data are returned to user on /oauth/state/ url.

The sender is the current user, parameters contain:

 * state - state (dictionary) being sent to the client. Normally it contains:

{
  "language": "cs",
  "loggedIn": true,
  "user": {
    "email": "simeki@vscht.cz",
    "id": 2,
    "roles": [
      {
        "id": "curator",
        "label": "Kur\u00e1tor dat"
      }
    ]
  },
  "userInfo": {
    "email": "simeki@vscht.cz",
    "familyName": "\u0160imek",
    "givenName": "Miroslav",
    "http://cis.vscht.cz/openid#metadata": [
    ],
    "name": "Miroslav \u0160imek",
    # other metadata here
  }
}

Implementation of this signal may modify the state
(for example, add metadata from other sources).
"""
