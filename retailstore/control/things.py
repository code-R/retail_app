import json
import falcon


class BaseResource(object):
    def to_json(self, body_dict):
        """
        Thin wrapper around json.dumps.

        providing the default=str config.
        """
        return json.dumps(body_dict, default=str)

class ThingsResource(BaseResource):

    def on_get(self, req, resp):
        doc = {
            'images': [
                {
                    'href': '/images/1eaf6ef1-7f2d-4ecc-a8d5-6e8adba7cc0e.png'
                }
            ]
        }
        resp.body = self.to_json(doc)
        resp.status = falcon.HTTP_200
