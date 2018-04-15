from retailstore.control import categories
from retailstore.db.sqlalchemy.models import Category
from retailstore.serializers.schemas import CategorySchema


def test_collection_properties(mocker):
    api = categories.CollectionResource()

    assert isinstance(api.get_schema, CategorySchema)
    assert isinstance(api.post_schema, CategorySchema)
    assert api.get_schema.many
    assert api.orm_model == Category

def test_item_properties(mocker):
    api = categories.ItemResource()

    assert isinstance(api.schema, CategorySchema)
    assert api.resource_key == 'category_id'
    assert api.orm_model == Category
