from retailstore.control.base import (
    CollectionBase,
    ItemResourceBase,
)
from retailstore.db.sqlalchemy.models import Category
from retailstore.serializers.schemas import CategorySchema


class CollectionResource(CollectionBase):
    get_schema = CategorySchema(many=True)
    post_schema = CategorySchema()
    orm_model = Category
    relationship_key = 'department_id'


class ItemResource(ItemResourceBase):

    schema = CategorySchema()
    orm_model = Category
    resource_key = 'category_id'
