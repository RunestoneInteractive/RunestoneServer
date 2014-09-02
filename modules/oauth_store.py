import oauth

class LTI_OAuthDataStore(oauth.OAuthDataStore):

    key = None
    secret = None

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret
        pass

    def lookup_consumer(self, key):
        if key == self.key :
            return oauth.OAuthConsumer(key, self.secret)
        return None

    # We don't do request_tokens
    def lookup_token(self, token_type, token):
        return oauth.OAuthToken(None, None)

    # Trust all nonces
    def lookup_nonce(self, oauth_consumer, oauth_token, nonce):
        return None

    # We don't do request_tokens
    def fetch_request_token(self, oauth_consumer):
        return None

    # We don't do request_tokens
    def fetch_access_token(self, oauth_consumer, oauth_token):
        return None

    # We don't do request_tokens
    def authorize_request_token(self, oauth_token, user):
        return None
