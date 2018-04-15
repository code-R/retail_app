import falcon
from mock import Mock
from sqlalchemy.orm import sessionmaker

from retailstore.control import locations
from retailstore.db.sqlalchemy.models import Location
from retailstore.serializers.schemas import LocationSchema


def test_get_locations(mocker):
    session = mocker.MagicMock(sessionmaker)
    Location.fetch_resources = Mock(return_value = ['this is test'])
    api = locations.CollectionResource(session)

    # Configure mocked request and response
    req = mocker.MagicMock(spec=falcon.Request)
    resp = mocker.MagicMock(spec=falcon.Response)

    api.on_get(req, resp)

    assert resp.body == ['this is test']
    assert resp.status == falcon.HTTP_200

def test_get_location(mocker):
    session = mocker.MagicMock(sessionmaker)
    Location.fetch_resource = Mock(return_value = 'location_obj')
    api = locations.ItemResource(session)

    # Configure mocked request and response
    req = mocker.MagicMock(spec=falcon.Request)
    resp = mocker.MagicMock(spec=falcon.Response)

    api.on_get(req, resp, location_id=1)

    assert resp.body == 'location_obj'
    assert resp.status == falcon.HTTP_200

def test_post_location(mocker):
    session = mocker.MagicMock(sessionmaker)()
    api = locations.CollectionResource(session)

    # Configure mocked request and response
    req = mocker.MagicMock(spec=falcon.Request)
    resp = mocker.MagicMock(spec=falcon.Response)

    api.on_post(req, resp)
    assert resp.status == falcon.HTTP_204

def test_delete_location(mocker):
    session = mocker.MagicMock(sessionmaker)()
    Location.fetch_resource = Mock(return_value = 'location_obj')
    api = locations.ItemResource(session)

    # Configure mocked request and response
    req = mocker.MagicMock(spec=falcon.Request)
    resp = mocker.MagicMock(spec=falcon.Response)

    api.on_delete(req, resp, location_id=1)
    assert resp.status == falcon.HTTP_202

def test_put_location(mocker):
    session = mocker.MagicMock(sessionmaker)()
    location_mock = mocker.MagicMock(Location)
    Location.fetch_resource = Mock(return_value = location_mock)
    api = locations.ItemResource(session)

    # Configure mocked request and response
    req = mocker.MagicMock(spec=falcon.Request)
    resp = mocker.MagicMock(spec=falcon.Response)

    api.on_put(req, resp, location_id=1)
    assert resp.status == falcon.HTTP_204

def test_collection_properties(mocker):
    api = locations.CollectionResource()

    assert isinstance(api.get_schema, LocationSchema)
    assert isinstance(api.post_schema, LocationSchema)
    assert api.get_schema.many
    assert api.orm_model == Location

def test_item_properties(mocker):
    api = locations.ItemResource()

    assert isinstance(api.schema, LocationSchema)
    assert api.resource_key == 'location_id'
    assert api.orm_model == Location
