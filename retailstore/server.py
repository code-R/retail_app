import os

import falcon
from falcon_marshmallow import Marshmallow

from retailstore.control import(
    locations,
)
from retailstore import errors


def configure_app(app, version=''):
    v1_0_routes = [
        ('locations', locations.CollectionResource()),
        ('locations/{location_id}', locations.ItemResource()),
    ]

    for path, res in v1_0_routes:
        app.add_route(os.path.join('/api/%s' % version, path), res)

    app.add_error_handler(Exception, errors.default_exception_handler)

    return app

# Initialization compatible with PasteDeploy
def api_app_factory(global_conf, disable=None):
    middlewares = [
        Marshmallow(),
    ]
    app = falcon.API(middleware=middlewares)
    wsgi_callable = configure_app(app, 'v1.0'),
    return wsgi_callable
