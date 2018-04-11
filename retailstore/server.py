import os
import falcon

from retailstore.control.things import ThingsResource
from retailstore import errors

def configure_app(app, version=''):
    v1_0_routes = [
        ('things', ThingsResource()),
    ]

    for path, res in v1_0_routes:
        app.add_route(os.path.join('/api/%s' % version, path), res)

    app.add_error_handler(Exception, errors.default_exception_handler)

    return app

# Initialization compatible with PasteDeploy
def api_app_factory(global_conf, disable=None):
    app = falcon.API()
    wsgi_callable = configure_app(app, 'v1.0'),
    return wsgi_callable
