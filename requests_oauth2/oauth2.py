import requests

from six.moves.urllib.parse import quote, urlencode, parse_qs

from requests_oauth2.errors import ConfigurationError


class OAuth2(object):
    client_id = None
    client_secret = None
    site = None
    redirect_uri = None
    authorization_url = '/oauth/authorize'
    token_url = '/oauth/token'
    revoke_url = '/oauth2/revoke'
    scope_sep = None

    def __init__(self, client_id=None, client_secret=None, site=None,
                 redirect_uri=None, authorization_url=None,
                 token_url=None, revoke_url=None, scope_sep=None):
        """
        Initializes the hook with OAuth2 parameters
        """
        if client_id is not None:
            self.client_id = client_id
        if client_secret is not None:
            self.client_secret = client_secret
        if site is not None:
            self.site = site
        if redirect_uri is not None:
            self.redirect_uri = redirect_uri
        if authorization_url is not None:
            self.authorization_url = authorization_url
        if token_url is not None:
            self.token_url = token_url
        if revoke_url is not None:
            self.revoke_url = revoke_url
        if scope_sep is not None:
            self.scope_sep = scope_sep

    def _check_configuration(self, *attrs):
        """Check that each named attr has been configured
        """
        for attr in attrs:
            if getattr(self, attr, None) is None:
                raise ConfigurationError("{} not configured".format(attr))

    def _make_request(self, url, **kwargs):
        """
        Make a request to an OAuth2 endpoint
        """
        response = requests.post(url, **kwargs)
        try:
            return response.json()
        except ValueError:
            pass
        return parse_qs(response.content)

    def authorize_url(self, scope='', **kwargs):
        """
        Returns the url to redirect the user to for user consent
        """
        self._check_configuration("site", "authorization_url", "redirect_uri",
                                  "client_id")
        if isinstance(scope, (list, tuple, set, frozenset)):
            self._check_configuration("scope_sep")
            scope = self.scope_sep.join(scope)
        oauth_params = {
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id,
            'scope': scope,
        }
        oauth_params.update(kwargs)
        return "%s%s?%s" % (self.site, quote(self.authorization_url),
                            urlencode(oauth_params))

    def get_token(self, code, headers=None, **kwargs):
        """
        Requests an access token
        """
        self._check_configuration("site", "token_url", "redirect_uri",
                                  "client_id", "client_secret")
        url = "%s%s" % (self.site, quote(self.token_url))
        data = {
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
        }
        data.update(kwargs)

        return self._make_request(url, data=data, headers=headers)

    def refresh_token(self, headers=None, **kwargs):
        """
        Request a refreshed token
        """
        self._check_configuration("site", "token_url", "client_id",
                                  "client_secret")
        url = "%s%s" % (self.site, quote(self.token_url))
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }
        data.update(kwargs)

        return self._make_request(url, data=data, headers=headers)

    def revoke_token(self, token, headers=None, **kwargs):
        """
        Revoke an access token
        """
        self._check_configuration("site", "revoke_uri")
        url = "%s%s" % (self.site, quote(self.revoke_url))
        data = {'token': token}
        data.update(kwargs)

        return self._make_request(url, data=data, headers=headers)
