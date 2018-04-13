import falcon
from marshmallow import fields, Schema
from sqlalchemy import orm

from retailstore.control.base import BaseResource
from retailstore.db.sqlalchemy.models import Location
from retailstore.errors import LocationNotFound

class LocationSchema(Schema):
    id = fields.Integer()
    name = fields.String()


class CollectionResource(BaseResource):
    get_schema = LocationSchema(many=True)
    post_schema = LocationSchema()

    def on_get(self, req, resp):
        locations = self.orm_session.query(Location).all()
        req.context['result'] = locations

    def on_post(self, req, resp):
        location = Location(**req.context['json'])
        self.orm_session.add(location)
        self.orm_session.commit()

class ItemResource(BaseResource):

    schema = LocationSchema()

    def on_get(self, req, resp, location_id):
        try:
            location = self.orm_session.query(
                Location).filter_by(id=location_id).one()
            req.context['result'] = location
        except orm.exc.NoResultFound:
            raise LocationNotFound(location_id=location_id)

    def on_put(self, req, resp, location_id):
        try:
            location = self.orm_session.query(
                Location).filter_by(id=location_id).one()
            location_info = req.context['json']
            location.name = location_info['name']
            self.orm_session.commit()
            resp.status = falcon.HTTP_204
            resp.location = req.path
        except orm.exc.NoResultFound:
            raise LocationNotFound(location_id=location_id)

    def on_delete(self, req, resp, location_id):
        try:
            location = self.orm_session.query(
                Location).filter_by(id=location_id).one()
            self.orm_session.delete(location)
            self.orm_session.commit()
            resp.status = falcon.HTTP_202
            resp.location = req.path
        except orm.exc.NoResultFound:
            raise LocationNotFound(location_id=location_id)
        pass
