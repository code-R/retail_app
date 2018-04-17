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
        options = {'verify_exp': True}
        try:
            jwt.decode(
                self.token,
                self.secret,
                verify='True',
                algorithms=['HS256'],
                options=options
            )
            return True
        except jwt.DecodeError:
            return False


class JwtAuthFilter:
    """PasteDeploy filter for Jwt Auth."""

    def __init__(self, app, exempted_routes):
        self.app = app[0]
        self.exempted_routes = [
            ('/api/v1.0/%s' % route)
            for route in exempted_routes
        ]

    @webob.dec.wsgify
    def __call__(self, req):
        if req.path in self.exempted_routes:
            return req.get_response(self.app)

        token = req.environ.get('HTTP_AUTHORIZATION').partition('Bearer ')[2]
        jwt_auth = JwtAuthentication(token)
        if jwt_auth.is_valid():
            response = req.get_response(self.app)
        else:
            response = webob.exc.HTTPUnauthorized()

        return response
