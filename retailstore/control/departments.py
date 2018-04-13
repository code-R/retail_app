import falcon
from marshmallow import fields, Schema
from sqlalchemy import orm

from retailstore.control.base import BaseResource
from retailstore.db.sqlalchemy.models import Department
from retailstore.errors import DepartmentNotFound

class DepartmentSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    location_id = fields.Integer()


class CollectionResource(BaseResource):
    get_schema = DepartmentSchema(many=True)
    post_schema = DepartmentSchema()

    def on_get(self, req, resp, location_id):
        locations = self.orm_session.query(Department).all()
        req.context['result'] = locations

    def on_post(self, req, resp, location_id):
        department_dict = req.context['json']
        department_dict['location_id'] = location_id
        department = Department(**req.context['json'])
        self.orm_session.add(department)
        self.orm_session.commit()

class ItemResource(BaseResource):

    schema = DepartmentSchema()

    def on_get(self, req, resp, location_id, department_id):
        try:
            location = self.orm_session.query(
                Department).filter_by(id=department_id).one()
            req.context['result'] = location
        except orm.exc.NoResultFound:
            raise DepartmentNotFound(department_id=department_id)

    def on_put(self, req, resp, location_id, department_id):
        try:
            location = self.orm_session.query(
                Department).filter_by(id=department_id).one()
            location_info = req.context['json']
            location.name = location_info['name']
            self.orm_session.commit()
            resp.status = falcon.HTTP_204
            resp.location = req.path
        except orm.exc.NoResultFound:
            raise DepartmentNotFound(department_id=department_id)

    def on_delete(self, req, resp, location_id, department_id):
        try:
            location = self.orm_session.query(
                Department).filter_by(id=department_id).one()
            self.orm_session.delete(location)
            self.orm_session.commit()
            resp.status = falcon.HTTP_202
            resp.location = req.path
        except orm.exc.NoResultFound:
            raise DepartmentNotFound(department_id=department_id)
        pass
