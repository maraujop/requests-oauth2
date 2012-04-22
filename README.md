# requests-oauth2

This plugins adds OAuth v2.0 support to <a href="http://github.com/kennethreitz">@kennethreitz</a> well-known <a href="http://github.com/kennethreitz/requests">requests</a> library.

requests-oauth2 wants to provide the simplest and easiest way to do OAuth2 in Python. OAuth2 is several orders of magnitude easier to do than old OAuth1.0, so this is basically a simple connection initialization library. If you are looking for a way of doing OAuth 1.0 see <a href="http://github.com/maraujop/requests-oauth">requests-oauth</a>

Author: <a href="http://github.com/maraujop">Miguel Araujo</a>
Licence: BSD

## Usage with Facebook API

Initialize the connection handler. It accepts this parameters. `authorization_url` and `token_url` are optional and have defaults.

    from oauth2 import OAuth2
    OAuth2(client_id, client_secret, site, redirect_uri, [authorization_url='oauth/authorize'], [token_url='oauth/token'])

An example for facebook would be:

    oauth2_handler = OAuth2(client_id, client_secret, "https://www.facebook.com/", "http://yoursite.com/webhook", "dialog/oauth", "oauth/access_token")

Get the url to redirect the user to for consenting OAuth2 application usage using `authorize_url`. This method can be passed a `scope`, which defines the permissions your application will have with that user. If not passed, an empty string will be used, which in some providers means default privileges:

    authorization_url = oauth2_handler.authorize_url('email')

You can pass named parameters to `authorize_url`. Some OAuth2 providers allow extra parameters for configuring authorization. For example in google api:

    authorization_url = oauth2_handler.authorize_url('https://www.googleapis.com/auth/books', response_type='code')

Once the user clicks in this `authorization_url`. He will be requested to log in, if he wasn't, and consent access to the application. After granting access, user will be redirected to `http://yoursite.com/webhook?params`. `params` are a list of GET params. If everything went right they should at least contain a param named `code`, you will need to parse it and pass it to the connection handler. 

The code will be used to request an access token, necessary for all following requests to the API you do. Sometimes the site for authorization is different to the site for user consent (`token_url`). You can change the site in between doing:

    oauth2_handler.site = "https://graph.facebook.com/"

Finally we have to get an access token passing the code we got from the OAuth provider, for that we use `get_token`. This method also accepts extra named parameters that you may need:

    response = oauth2_handler.get_token(code)

Response can be a dictionary or `None`, if everything went right it should contain at least an `access_token` key. It will usually contain other interesting parameters such as expiring time. We can now do API calls, all of them should contain the `access_token` as a parameter. Thus we can generate a requests session, to avoid passing the parameter every time.

    oauth2_client = requests.session(params={'access_token': response['access_token']})
    oauth2_client.get('https://graph.facebook.com/me')

## Next

From here you can code your own binding for your favorite API the way you like. This will usually imply persisting the access token mapped to some user's information, so you can replicate the session on every request. Also you will have to handle error situations and token expiration, for sure requests will help you tackle this task.

There are also many API bindings available that will start requesting you an access token, but won't do the OAuth2 initialization handling for you, then requests-oauth2 will prove useful.

## Interesting readings

* Using OAuth 2.0 to Access Google APIs:
https://developers.google.com/accounts/docs/OAuth2

* Using OAuth 2.0 for Web Server Applications Google APIs:
https://developers.google.com/accounts/docs/OAuth2WebServer

* OAuth 2.0 in Facebook:
http://developers.facebook.com/docs/authentication/

* Github OAuth 2.0 usage:
http://develop.github.com/p/oauth.html

* You can use postbin for testing webhooks:
http://www.postbin.org/
