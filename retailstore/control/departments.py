from retailstore.control.base import (
    CollectionBase,
    ItemResourceBase,
)
from retailstore.db.sqlalchemy.models import Department
from retailstore.serializers.schemas import DepartmentSchema


class CollectionResource(CollectionBase):
    get_schema = DepartmentSchema(many=True)
    post_schema = DepartmentSchema()
    orm_model = Department


class ItemResource(ItemResourceBase):
    schema = DepartmentSchema()
    orm_model = Department
    resource_key = 'department_id'
