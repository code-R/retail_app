import falcon

from retailstore.control.base import BaseResource
from retailstore.control.auth import AuthService


class TokenResource(BaseResource):

    def on_post(self, req, resp):
        auth_service = AuthService(req.context['json'])

        if auth_service.valid():
            resp.body = auth_service.token_info.to_json()
            resp.status = falcon.HTTP_201
        else:
            resp.status = falcon.HTTP_401
