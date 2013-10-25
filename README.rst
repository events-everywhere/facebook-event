Facebook-event
==============
Simple Python command line script for creating, updating and displaying Facebook events.

Requirements
------------
`facepy <https://pypi.python.org/pypi/facepy>`
`requests <https://pypi.python.org/pypi/requests>` (required by facepy)

Obtaining access tokens
-----------------------
*Only user token allows to post events on behalf of the user*

App token:

1. Go to: https://developers.facebook.com/apps
2. Click: "Create New App"
3. Provide an app name, then click "Continue"
4. Token is available at: https://developers.facebook.com/tools/access_token/

Extended user token (complete above before proceeding):
Go to: https://developers.facebook.com/tools/explorer
Select your application and click: "Get Access Token"
Check: "user_events" (in "User Data Permissions") and "create_event" (in "Extended Permissions")
Click: "Get Access Token"

This is short-lived token (which expires in about 2 hours). 
To extend it (to about 2 months) you need use facebook-extend-access-token.py script together with the 
just generated short-lived token, app id and app secret (https://developers.facebook.com/apps):

.. code-block:: bash

    $ ./facebook-extend-access-token.py --appid 'App ID' --appsecret 'App Secret' --token 'User Token'

For more details, please go to:
`<https://developers.facebook.com/docs/facebook-login/access-tokens>`

Command examples
----------------
*All examples assume you have already setup your access token in config.json!*

.. code-block:: bash

    $ ./facebook-event.py -h
    $ ./facebook-event.py create --title 'Event title' --desc 'Event description' --date '2013-11-11 16:16'
    $ ./facebook-event.py update --id 331218348435 --desc 'Event description update'
    $ ./facebook-event.py details --id 'https://www.facebook.com/events/331218348435'
    $ ./facebook-event.py details --id 331218348435

