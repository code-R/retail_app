import falcon
from sqlalchemy.exc import IntegrityError

from retailstore.control.base import BaseResource
from retailstore.db.sqlalchemy.models import Location
from retailstore.serializers.schemas import LocationSchema
from retailstore.errors import DuplicationLocation

class CollectionResource(BaseResource):
    get_schema = LocationSchema(many=True)
    post_schema = LocationSchema()

    def on_get(self, req, resp):
        locations = self.orm_session.query(Location).all()
        req.context['result'] = locations

    def on_post(self, req, resp):
        location = Location(**req.context['json'])
        self.orm_session.add(location)
        try:
            self.orm_session.commit()
        except IntegrityError:
            self.orm_session.rollback()
            raise DuplicationLocation()
        resp.status = falcon.HTTP_204


class ItemResource(BaseResource):

    schema = LocationSchema()

    def on_get(self, req, resp, location_id):
        location = self._get_location(location_id)
        req.context['result'] = location

    def on_put(self, req, resp, location_id):
        location = self._get_location(location_id)
        location_info = req.context['json']
        location.name = location_info['name']
        location.description = location_info['description']
        self.orm_session.commit()
        resp.status = falcon.HTTP_204

    def on_delete(self, req, resp, location_id):
        location = self._get_location(location_id)
        self.orm_session.delete(location)
        self.orm_session.commit()
        resp.status = falcon.HTTP_202
