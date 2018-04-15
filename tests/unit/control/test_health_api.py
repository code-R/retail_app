import falcon
from sqlalchemy.orm import sessionmaker

from retailstore.control.health import HealthResource


def test_get_health(mocker):
    session = mocker.MagicMock(sessionmaker)
    api = HealthResource(session)

    # Configure mocked request and response
    req = mocker.MagicMock(spec=falcon.Request)
    resp = mocker.MagicMock(spec=falcon.Response)
    api.on_get(req, resp)

    assert resp.status == falcon.HTTP_204
