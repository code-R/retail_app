"""Test Things API."""

from retailstore.control.things import ThingsResource

import falcon


def test_get_things(mocker):
    api = ThingsResource()

    # Configure mocked request and response
    req = mocker.MagicMock(spec=falcon.Request)
    resp = mocker.MagicMock(spec=falcon.Response)

    api.on_get(req, resp)

    doc = {
        'images': [{
            'href': '/images/1eaf6ef1-7f2d-4ecc-a8d5-6e8adba7cc0e.png'
        }]
    }
    expected = api.to_json(doc)

    assert resp.body == expected
    assert resp.status == falcon.HTTP_200
