import falcon
from sqlalchemy.exc import IntegrityError

from retailstore.db.sqlalchemy import api as db_api
from retailstore.errors import (
    DuplicationResource,
)


class BaseResource(object):
    def __init__(self):
        self.orm_session = db_api.get_session()

    def _get_resource(self, *args, **kwargs):
        return self.orm_model.fetch_resource(self.orm_session, **kwargs)


class CollectionBase(BaseResource):
    def on_get(self, req, resp, *args, **kwargs):
        resources = self.orm_model.fetch_resources(self.orm_session, **kwargs)
        req.context['result'] = resources

    def on_post(self, req, resp, *args, **kwargs):
        resource_dict = req.context['json']
        resource_dict.update(kwargs)
        resource = self.orm_model(**resource_dict)
        self.orm_session.add(resource)
        try:
            self.orm_session.commit()
        except IntegrityError:
            self.orm_session.rollback()
            raise DuplicationResource(table=self.orm_model.__tablename__)

        resp.status = falcon.HTTP_204


class ItemResourceBase(BaseResource):
    def on_get(self, req, resp, *args, **kwargs):
        query_dict = kwargs
        query_dict['id'] = query_dict.pop(self.resource_key)
        resource = self._get_resource(**query_dict)
        req.context['result'] = resource

    def on_delete(self, req, resp, *args, **kwargs):
        query_dict = kwargs
        query_dict['id'] = query_dict.pop(self.resource_key)
        resource = self._get_resource(**query_dict)
        self.orm_session.delete(resource)
        self.orm_session.commit()
        resp.status = falcon.HTTP_202

    def on_put(self, req, resp, *args, **kwargs):
        query_dict = kwargs
        query_dict['id'] = query_dict.pop(self.resource_key)
        resource = self._get_resource(**query_dict)
        resource_dict = req.context['json']
        resource_dict.update(kwargs)
        resource.name = resource_dict['name']
        resource.description = resource_dict['description']
        self.orm_session.commit()
        resp.status = falcon.HTTP_204
        resp.location = req.path
