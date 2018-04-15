import falcon
from sqlalchemy.exc import IntegrityError

from retailstore.db.sqlalchemy import api as db_api
from retailstore.errors import (
    DuplicationResource,
)


class BaseResource(object):
    def __init__(self, session=None):
        if session:
            self.orm_session = session
        else:
            self.orm_session = db_api.get_session()

    def _get_resource(self, *args, **kwargs):
        query_dict = kwargs.copy()
        query_dict['id'] = query_dict.pop(self.resource_key)
        return self.orm_model.fetch_resource(self.orm_session, **query_dict)


class CollectionBase(BaseResource):
    def on_get(self, req, resp, *args, **kwargs):
        resources = self.orm_model.fetch_resources(self.orm_session, **kwargs)
        req.context['result'] = resources
        resp.body = resources
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp, *args, **kwargs):
        resource_dict = req.context['json'].copy()
        if hasattr(self, 'relationship_key'):
            resource_dict[self.relationship_key] = \
                kwargs[self.relationship_key]
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
        resource = self._get_resource(**kwargs)
        req.context['result'] = resource
        resp.body = resource
        resp.status = falcon.HTTP_200

    def on_delete(self, req, resp, *args, **kwargs):
        resource = self._get_resource(**kwargs)
        self.orm_session.delete(resource)
        self.orm_session.commit()
        resp.status = falcon.HTTP_202

    def on_put(self, req, resp, *args, **kwargs):
        resource = self._get_resource(**kwargs)
        resource_dict = req.context['json']
        resource_dict.update(kwargs)
        resource.name = resource_dict['name']
        resource.description = resource_dict['description']
        self.orm_session.commit()
        resp.status = falcon.HTTP_204
