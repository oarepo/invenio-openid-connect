# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET z.s.p.o..
#
# OARepo is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""Definition of state view."""

import humps
from flask import Blueprint, Response, jsonify, make_response, session, request
from flask_babelex import get_locale, gettext, refresh
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


@blueprint.route('/complete/')
def complete():
    """
    Redirect to this url after login has been completed to pass the login info.

    This url is called by @oarepo/vue-popup-login after login to notify the main window
    that the login process has been finished.

    :return: http message with a bit of javascript
    """
    if current_user.is_authenticated:
        login_complete = gettext("Login complete")
        user_logged_in = gettext("The login process has been completed "
                                 "and %(user)s has been logged in.", user=session['user_info']['name'])
        close_window = gettext("This window should close automatically in a second.")
        cannot_send_data = gettext("Could not send login data back to the application. "
                                   "Please close this window manually and reload the application")
        if request.args.get('next'):
            redirecting = gettext('You are being redirected to the application. '
                                  'If it does not happen in a couple of seconds, '
                                  'click <a href="%(next)s">here</a>. ', next=request.args.get('next'))
            resp = make_response(f"""
                <html>
                    <body style="display: flex; justify-content: center;">
                        <div style="max-width: 400px;">
                            <h3 style="border-bottom: 1px solid darkgreen; text-align: center; margin-bottom: 40px">
                                {login_complete}
                            </h3>
                            <div style="padding-top: 10px; padding-bottom: 10px;">
                                {user_logged_in}
                                <br><br>
                                {redirecting}
                            </div>
                        </div>
                    </body>
                </html>
            """, 302)
            resp.headers['Location'] = request.args.get('next')
            return resp
        else:
            return make_response(f"""
                <html>
                    <head>
                       {broadcast_channel_polyfill}
                    </head>
                    <body style="display: flex; justify-content: center;">
                        <div style="max-width: 400px;">
                            <h3 style="border-bottom: 1px solid darkgreen; text-align: center; margin-bottom: 40px">
                                {login_complete}
                            </h3>
                            <div style="padding-top: 10px; padding-bottom: 10px;">
                                {user_logged_in}
                                <br><br>
                                {close_window}
                            </div>
                            <script>
                                setTimeout(() => {{
                                    const bc = new BroadcastChannel('popup-login-channel');
                                    bc.postMessage({{
                                        type: "login",
                                        status: "${{state.authState.loggedIn ? 'success' : 'error'}}",
                                        message: ""
                                    }})
                                    setTimeout(() => {{
                                        alert('{cannot_send_data}')
                                    }}, 5000)
                                }}, 1000)
                            </script>
                        </div>
                    </body>
                </html>
            """)
    else:
        auth_failed = gettext("Authentication failed")
        failed_expl = gettext("The authentication process failed. "
                              "Please, close the application, reopen it and try again.")
        support = gettext("If it does not help, please call the technical support.")
        return make_response(f"""
            <html>
                <body style="display: flex; justify-content: center;">
                    <div style="max-width: 400px;">
                        <h3 style="border-bottom: 1px solid darkgreen; text-align: center; margin-bottom: 40px">
                            {auth_failed}
                        </h3>
                        <div style="padding-top: 10px; padding-bottom: 10px;">
                            {failed_expl}
                            <br><br>
                            {support}
                        </div>
                    </div>
                </body>
            </html>
        """)


broadcast_channel_polyfill = """
<script>
// https://www.npmjs.com/package/broadcastchannel-polyfill
(function(global) {
    var channels = [];

    function BroadcastChannel(channel) {
        var $this = this;
        channel = String(channel);

        var id = '$BroadcastChannel$' + channel + '$';

        channels[id] = channels[id] || [];
        channels[id].push(this);

        this._name = channel;
        this._id = id;
        this._closed = false;
        this._mc = new MessageChannel();
        this._mc.port1.start();
        this._mc.port2.start();

        global.addEventListener('storage', function(e) {
            if (e.storageArea !== global.localStorage) return;
            if (e.newValue == null || e.newValue === '') return;
            if (e.key.substring(0, id.length) !== id) return;
            var data = JSON.parse(e.newValue);
            $this._mc.port2.postMessage(data);
        });
    }

    BroadcastChannel.prototype = {
        // BroadcastChannel API
        get name() {
            return this._name;
        },
        postMessage: function(message) {
            var $this = this;
            if (this._closed) {
                var e = new Error();
                e.name = 'InvalidStateError';
                throw e;
            }
            var value = JSON.stringify(message);

            // Broadcast to other contexts via storage events...
            var key = this._id + String(Date.now()) + '$' + String(Math.random());
            global.localStorage.setItem(key, value);
            setTimeout(function() {
                global.localStorage.removeItem(key);
            }, 500);

            // Broadcast to current context via ports
            channels[this._id].forEach(function(bc) {
                if (bc === $this) return;
                bc._mc.port2.postMessage(JSON.parse(value));
            });
        },
        close: function() {
            if (this._closed) return;
            this._closed = true;
            this._mc.port1.close();
            this._mc.port2.close();

            var index = channels[this._id].indexOf(this);
            channels[this._id].splice(index, 1);
        },

        // EventTarget API
        get onmessage() {
            return this._mc.port1.onmessage;
        },
        set onmessage(value) {
            this._mc.port1.onmessage = value;
        },
        addEventListener: function(/*type, listener , useCapture*/) {
            return this._mc.port1.addEventListener.apply(this._mc.port1, arguments);
        },
        removeEventListener: function(/*type, listener , useCapture*/) {
            return this._mc.port1.removeEventListener.apply(this._mc.port1, arguments);
        },
        dispatchEvent: function(/*event*/) {
            return this._mc.port1.dispatchEvent.apply(this._mc.port1, arguments);
        },
    };

    global.BroadcastChannel = global.BroadcastChannel || BroadcastChannel;
})(self);
</script>
"""
