import requests
from urllib import quote, urlencode
from urlparse import parse_qs
try:
    import simplejson as json
except ImportError:
    import json


class OAuth2(object):
    authorization_url = '/oauth/authorize'
    token_url = '/oauth/token'

    def __init__(self, client_id, client_secret, site, redirect_uri, authorization_url=None, token_url=None):
        """
        Initializes the hook with OAuth2 parameters
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.site = site
        self.redirect_uri = redirect_uri
        if authorization_url is not None:
            self.authorization_url = authorization_url
        if token_url is not None:
            self.token_url = token_url

    def authorize_url(self, scope='', **kwargs):
        """
        Returns the url to redirect the user to for user consent
        """
        oauth_params = {'redirect_uri': self.redirect_uri, 'client_id': self.client_id, 'scope': scope}
        oauth_params.update(kwargs)
        return "%s%s?%s" % (self.site, quote(self.authorization_url), urlencode(oauth_params))

    def get_token(self, code, **kwargs):
        """
        Requests an access token
        """
        url = "%s%s" % (self.site, quote(self.token_url))
        data = {'redirect_uri': self.redirect_uri, 'client_id': self.client_id, 'client_secret': self.client_secret, 'code': code}
        data.update(kwargs)
        response = requests.post(url, data=data)

        if isinstance(response.content, basestring):
            try:
                content = json.loads(response.content)
            except ValueError:
                content = parse_qs(response.content)
        else:
            content = response.content

        return content
