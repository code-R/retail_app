from sqlalchemy.orm import sessionmaker

from retailstore.control import sub_categories
from retailstore.db.sqlalchemy.models import SubCategory
from retailstore.serializers.schemas import SubCategorySchema


def test_collection_properties(mocker):
    session = mocker.MagicMock(sessionmaker)
    api = sub_categories.CollectionResource(session)

    assert isinstance(api.get_schema, SubCategorySchema)
    assert isinstance(api.post_schema, SubCategorySchema)
    assert api.get_schema.many
    assert api.orm_model == SubCategory

def test_item_properties(mocker):
    session = mocker.MagicMock(sessionmaker)
    api = sub_categories.ItemResource(session)

    assert isinstance(api.schema, SubCategorySchema)
    assert api.resource_key == 'sub_category_id'
    assert api.orm_model == SubCategory
