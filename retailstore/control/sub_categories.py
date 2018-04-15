from retailstore.control.base import (
    CollectionBase,
    ItemResourceBase,
)
from retailstore.db.sqlalchemy.models import SubCategory
from retailstore.serializers.schemas import SubCategorySchema


class CollectionResource(CollectionBase):
    get_schema = SubCategorySchema(many=True)
    post_schema = SubCategorySchema()
    orm_model = SubCategory


class ItemResource(ItemResourceBase):

    schema = SubCategorySchema()
    orm_model = SubCategory
    resource_key = 'sub_category_id'
