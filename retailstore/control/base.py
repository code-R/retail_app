import json

from retailstore.db.sqlalchemy import api as db_api


class BaseResource(object):
    def __init__(self):
        self.orm_session = db_api.get_session()

    def to_json(self, body_dict):
        return json.dumps(body_dict, default=str)
