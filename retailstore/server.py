import os

import falcon
from falcon_marshmallow import Marshmallow

from retailstore.control import (
    locations,
    departments,
    health,
    hiera,
    categories,
    sub_categories,
)
from retailstore import errors


def configure_app(app, version=''):
    v1_0_routes = [
        ('health', health.HealthResource()),
        ('locations', locations.CollectionResource()),
        ('locations/{location_id}', locations.ItemResource()),
        ('locations/{location_id}/hiera_data', hiera.ItemResource()),
        (
            'locations/{location_id}/departments',
            departments.CollectionResource()
        ),
        (
            'locations/{location_id}/departments/{department_id}',
            departments.ItemResource()
        ),
        (
            'locations/{location_id}/departments/{department_id}/categories',
            categories.CollectionResource()
        ),
        (
            ('locations/{location_id}/departments/{department_id}'
                '/categories/{category_id}'),
            categories.ItemResource()
        ),
        (
            ('locations/{location_id}/departments/{department_id}/categories/'
                '{category_id}/sub_categories'),
            sub_categories.CollectionResource()
        ),
        (
            ('locations/{location_id}/departments/{department_id}/categories/'
                '{category_id}/sub_categories/{sub_category_id}'),
            sub_categories.ItemResource()
        ),
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
