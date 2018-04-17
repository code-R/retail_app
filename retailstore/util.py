import falcon

from retailstore.middleware.jwt import JwtAuthFilter

class BasicAuthFilter(object):
    """PasteDeploy filter for Basic Http Auth."""

    def __init__(self, app):
        self.app = app[0]

    def __call__(self, environ, start_response):
        basic_auth_token = 'open-sesame'
        header_auth_token = environ.get('HTTP_X_AUTH_TOKEN', basic_auth_token)
        if header_auth_token == basic_auth_token:
            return [self.app(environ, start_response)]
        else:
            raise falcon.HTTPUnauthorized()


def basic_auth_filter_factory(global_config, **local_config):
    """Paste Auth filter factory."""
    def auth_filter(app):
        return BasicAuthFilter(app)

    return auth_filter


def jwt_auth_filter_factory(global_config, exempted_routes=''):
    """Paste Jwt Auth filter factory."""
    def auth_filter(app):
        return JwtAuthFilter(app, exempted_routes.split())

    return auth_filter
