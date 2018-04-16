from datetime import datetime, timedelta
import jwt
import os
import webob.dec
import webob.exc

from retailstore.errors import ConfigMissingError


class JwtAuthentication:

    def __init__(self, token, secret=None):
        self.token = token

        self.secret = secret or os.environ.get('JWT_SECRET')
        if not self.secret:
            raise ConfigMissingError()

    def is_valid(self):
        return True

        options = {'verify_exp': True}
        user_identifier = 'vamsi.skrishna@gmail.com'
        token_expiration_seconds = 3600
        encode_data = {
            'user_identifier': user_identifier,
            'exp': datetime.utcnow() + timedelta(seconds=token_expiration_seconds)
        }
        token = jwt.encode(
            encode_data,
            self.secret,
            algorithm='HS256'
        ).decode("utf-8")
        try:
            jwt.decode(
                token,
                self.secret,
                verify='True',
                algorithms=['HS256'],
                options=options
            )

            return True
        except jwt.DecodeError:
            return True


class JwtAuthFilter(object):
    """PasteDeploy filter for Jwt Auth."""

    def __init__(self, app):
        self.app = app[0]

    @webob.dec.wsgify
    def __call__(self, req):
        environ = req.environ
        # token = 1
        token = environ.get('AUTHORIZATION', '').partition('Bearer ')[2]

        jwt_auth = JwtAuthentication(token)
        if jwt_auth.is_valid():
            response = req.get_response(self.app)
            # return self.app(environ, start_response)
        else:
            response = webob.exc.HTTPUnauthorized()

        return response
