# requests-oauth2

[![PyPI](https://img.shields.io/pypi/v/requests-oauth2.svg)](https://pypi.python.org/pypi/requests-oauth2)

OAuth v2.0 support for
[kennethreitz](https://github.com/kennethreitz)'s well-known
[Requests](https://github.com/kennethreitz/requests) library.

This library wants to provide the simplest and easiest way to do
OAuth2 in Python. OAuth2 is much easier to do than old OAuth1.0, and
likewise this library is simple, free of cruft, and practical in
everyday use. If you are looking for a way of doing OAuth 1.0, see
[requests-oauth](https://github.com/maraujop/requests-oauth).

Authors: see [AUTHORS](/AUTHORS).

License: BSD

Examples: with [Flask](/examples/web_flask.py).

## OAuth2 web app flow - the theory

Skip this if you know how OAuth2 works.

1. Your web app (*Foo*) allows users to log in with their *Qux*
   account. *Qux* here is a service provider; they gave you a **client
   ID** and a **secret key**, which *Foo* stores somewhere on the
   backend. *Qux* and *Foo* pre-agree on some **redirect URI**.
2. User visits *Foo*'s login screen, e.g.
   `https://www.foo.example/login`
3. *Foo* redirects users to *Qux*'s **Authorization URL**, e.g.
   `https://api.qux.example/oauth/authorize`
4. User is presented with *Qux*'s **consent screen**, where they
   review the **scope** of requested permissions, and either allow or
   deny access.
5. Once access is granted, *Qux* redirects back to *Foo* via the
   **redirect URI** that they both agreed upon beforehand, supplying
   the **code**.
6. *Foo* exchanges the **code** for an **access token**. The access
   token can be used by *Foo* to make API calls to *Qux* on user's
   behalf.

## Usage example

Look into the [examples directory](/examples) for fully integrated,
working examples.

Some providers are included out of the box, but adding more is quite
easy. In this example, we'll get started with Google.

You will find **Client ID** & **secret** (point 1 above) in your
[Google API console](https://console.cloud.google.com/apis/credentials).

You must choose the **redirect URI**, which must be handled by your
web app.

```python
from requests_oauth2.services import GoogleClient
google_auth = GoogleClient(
    client_id="your-google-client-id",
    client_secret="super-secret",
    redirect_uri="http://localhost:5000/google/oauth2callback",
)
```

When the user visits the login page (point 2), we'll build an
**authorization URL** (point 3) that will direct the user to Google's
**consent screen**, asking to grant the specified **scopes** (point
4):

```python
authorization_url = google_auth.authorize_url(
    scope=["email"],
    response_type="code",
)
```

Once the user clicks "allow", Google will redirect them to the
**redirect URI** (point 5), which will include the **code** as one of
the query string parameters:

    http://localhost:5000/google/oauth2callback?code=...

The code will be used to request an **access token** (point 6),
necessary for all following requests to the API:

```python
code = get_request_parameter("code")  # this depends on your web framework!
data = google_auth.get_token(
    code=code,
    grant_type="authorization_code",
)
```

You can store it somewhere for later use, e.g. in the session, or in
the database:

```python
session["access_token"] = data["access_token"]
```

The exact method for supplying the **access token** varies from one
provider to another. One popular method (supported by Google) is via
the Bearer header. There's a helper shortcut for this:

```python
from requests_oauth2 import OAuth2BearerToken

with requests.Session() as s:
    s.auth = OAuth2BearerToken(access_token)
    r = s.get("https://www.googleapis.com/plus/v1/people/me")
    r.raise_for_status()
    data = r.json()
```

Other providers, such as Facebook, allow the access token to be passed
as a request parameter (in the query string). You would so something
like this:

```python
from requests_oauth2 import OAuth2BearerToken

with requests.Session() as s:
    s.params = {"access_token": response["access_token"]}
    r = s.get("https://graph.facebook.com/me")
    r.raise_for_status()
    data = r.json()
```

## Interesting readings

* Using OAuth 2.0 to Access Google APIs:
  <https://developers.google.com/accounts/docs/OAuth2>

* Using OAuth 2.0 for Web Server Applications Google APIs:
  <https://developers.google.com/accounts/docs/OAuth2WebServer>

* OAuth 2.0 in Facebook:
  <http://developers.facebook.com/docs/authentication/>

* Github OAuth 2.0 usage:
  <https://developer.github.com/apps/building-oauth-apps/>

* You can use postbin for testing webhooks: <http://www.postbin.org/>
