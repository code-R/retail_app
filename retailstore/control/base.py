from sqlalchemy import orm

from retailstore.db.sqlalchemy import api as db_api
from retailstore.db.sqlalchemy.models import (
    Location,
    Department,
)
from retailstore.errors import (
    LocationNotFound,
    DepartmentNotFound,
)


class BaseResource(object):
    def __init__(self):
        self.orm_session = db_api.get_session()

    def _get_location(self, location_id):
        try:
            location = self.orm_session.query(
                Location).filter_by(id=location_id).one()
        except orm.exc.NoResultFound:
            raise LocationNotFound(location_id=location_id)

        return location

    def _get_department(self, location_id, department_id):
        try:
            department = self.orm_session.query(Department).filter_by(
                id=department_id, location_id=location_id).one()
        except orm.exc.NoResultFound:
            raise DepartmentNotFound(location_id=location_id)

        return department
