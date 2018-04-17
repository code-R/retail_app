import falcon
import json
from sqlalchemy import orm

from retailstore.control.base import BaseResource
from retailstore.serializers.schemas import LocationSchema
from retailstore.db.sqlalchemy.models import Location
from retailstore.errors import ResourceNotFound


class ItemResource(BaseResource):
    """This gives in depth view of all nested data."""

    def on_get(self, req, resp, location_id):
        try:
            location = self.orm_session.query(
                Location).filter_by(id=location_id).one()
        except orm.exc.NoResultFound:
            raise ResourceNotFound(
                message='this is my message, make it better')

        schema = LocationSchema()
        res = schema.hiera_data(location)
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(res)
