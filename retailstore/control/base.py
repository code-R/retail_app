import json


class BaseResource(object):
    def to_json(self, body_dict):
        return json.dumps(body_dict, default=str)
