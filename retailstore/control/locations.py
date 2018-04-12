from marshmallow import fields, Schema
from sqlalchemy import orm

from retailstore.control.base import BaseResource
from retailstore.db.sqlalchemy.models import Location
from retailstore.errors import LocationNotFound

class LocationSchema(Schema):
    id = fields.Integer()
    name = fields.String()


class CollectionResource(BaseResource):

    schema = LocationSchema(many=True)

    def on_get(self, req, resp):
        locations = self.orm_session.query(Location).all()
        req.context['result'] = locations


class ItemResource(BaseResource):

    schema = LocationSchema()

    def on_get(self, req, resp, location_id):
        try:
            location = self.orm_session.query(
                Location).filter_by(id=location_id).one()
            req.context['result'] = location
        except orm.exc.NoResultFound:
            raise LocationNotFound(location_id=location_id)
