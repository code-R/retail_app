import falcon

from retailstore.control.base import BaseResource

from retailstore.db.sqlalchemy import api as db_api
from retailstore.db.sqlalchemy.models import Location


class LocationsResource(BaseResource):

    def on_get(self, req, resp):
        session = db_api.get_session()
        locations = session.query(Location).all()

        resp.body = self.to_json(locations)
        resp.status = falcon.HTTP_200
