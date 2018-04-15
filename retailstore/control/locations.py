from retailstore.control.base import (
    CollectionBase,
    ItemResourceBase,
)
from retailstore.db.sqlalchemy.models import Location
from retailstore.serializers.schemas import LocationSchema


class CollectionResource(CollectionBase):
    get_schema = LocationSchema(many=True)
    post_schema = LocationSchema()
    orm_model = Location


class ItemResource(ItemResourceBase):

    schema = LocationSchema()
    orm_model = Location
    resource_key = 'location_id'
