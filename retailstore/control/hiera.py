import falcon
import json

from retailstore.control.base import BaseResource
from retailstore.serializers.schemas import LocationSchema


class ItemResource(BaseResource):
    """This gives in depth view of all nested data."""

    def on_get(self, req, resp, location_id):
        location = self._get_location(location_id)
        schema = LocationSchema()
        # schema.hiera_data(location)
        resp.status = falcon.HTTP_200
        res = schema.hiera_data(location)

        resp.body = json.dumps(res)
