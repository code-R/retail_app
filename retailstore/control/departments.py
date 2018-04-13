import falcon

from retailstore.control.base import BaseResource
from retailstore.db.sqlalchemy.models import Department
from retailstore.serializers.schemas import DepartmentSchema


class CollectionResource(BaseResource):
    get_schema = DepartmentSchema(many=True)
    post_schema = DepartmentSchema()

    def on_get(self, req, resp, department_id):
        departments = self.orm_session.query(Department).all()
        req.context['result'] = departments

    def on_post(self, req, resp, location_id):
        location = self._get_location(self, location_id)
        department = Department(**req.context['json'])
        department.location = location
        self.orm_session.add(department)
        self.orm_session.commit()


class ItemResource(BaseResource):

    schema = DepartmentSchema()

    def on_get(self, req, resp, location_id, department_id):
        department = self._get_department(location_id, department_id)
        req.context['result'] = department

    def on_put(self, req, resp, location_id, department_id):
        department = self._get_department(location_id, department_id)
        department_info = req.context['json']
        department.name = department_info['name']
        self.orm_session.commit()
        resp.status = falcon.HTTP_204
        resp.location = req.path

    def on_delete(self, req, resp, location_id, department_id):
        department = self._get_department(location_id, department_id)
        self.orm_session.delete(department)
        self.orm_session.commit()
        resp.status = falcon.HTTP_202
