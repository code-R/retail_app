# from webob import exc

# class AuthFilter(object):
#     """PasteDeploy filter for Basic Http Auth"""

#     def __init__(self, app, conf):
#         self.app = app
#         self.conf = conf

#     def __call__(self, environ, start_response):
#         if environ.get('HTTP_X_AUTH_TOKEN') == 'open-sesame':
#             return self.app(environ, start_response)
#         else:
#             return exc.HTTPForbidden()

# def auth_filter_factory(global_conf, **local_conf):
#     conf = global_conf.copy()
#     conf.update(local_conf)

#     def auth_filter(app):
#         return AuthFilter(app, conf)
#     return auth_filter


from webob.dec import wsgify
from webob import exc

@wsgify.middleware
def auth_filter(request, app):
    if request.headers.get('X-Auth-Token') != 'open-sesame':
        return exc.HTTPForbidden()
    return app(request)

def auth_filter_factory(global_config, **local_config):
    return auth_filter