from retailstore.control import departments
from retailstore.db.sqlalchemy.models import Department
from retailstore.serializers.schemas import DepartmentSchema


def test_collection_properties(mocker):
    api = departments.CollectionResource()

    assert isinstance(api.get_schema, DepartmentSchema)
    assert isinstance(api.post_schema, DepartmentSchema)
    assert api.get_schema.many
    assert api.orm_model == Department

def test_item_properties(mocker):
    api = departments.ItemResource()

    assert isinstance(api.schema, DepartmentSchema)
    assert api.resource_key == 'department_id'
    assert api.orm_model == Department
