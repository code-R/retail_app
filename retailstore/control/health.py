import falcon

from retailstore.control.base import BaseResource


class HealthResource(BaseResource):
    """Basic health check for Rstore.

    The response must be returned within 30 seconds
    for Rstore to be deemed "healthy".
    """

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_204
