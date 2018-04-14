from sqlalchemy.orm.exc import NoResultFound

from retailstore.db.sqlalchemy import api as db_api
from retailstore.db.sqlalchemy.models import (
    Location,
    Department,
    Category,
    SubCategory,
)


session = db_api.get_session()

def _get_one_or_create(model, **kwargs):
    try:
        return session.query(model).filter_by(**kwargs).one()
    except NoResultFound:
        return model(**kwargs)

def location_srv(data):
    replicated_data = data.copy()
    loc_obj = _get_one_or_create(Location, name=replicated_data['LOCATION'])
    session.add(loc_obj)
    session.commit()
    replicated_data['location_id'] = loc_obj.id
    return replicated_data

def department_srv(data):
    replicated_data = data.copy()
    dep_obj = _get_one_or_create(Department, name=replicated_data['DEPARTMENT'])
    dep_obj.location_id = replicated_data['location_id']
    session.add(dep_obj)
    session.commit()
    replicated_data['department_id'] = dep_obj.id
    return replicated_data

def category_srv(data):
    replicated_data = data.copy()
    dep_obj = _get_one_or_create(Category, name=replicated_data['CATEGORY'])
    dep_obj.department_id = replicated_data['department_id']
    session.add(dep_obj)
    session.commit()
    replicated_data['category_id'] = dep_obj.id
    return replicated_data

def sub_category_srv(data):
    replicated_data = data.copy()
    dep_obj = _get_one_or_create(SubCategory, name=replicated_data['SUBCATEGORY'])
    dep_obj.category_id = replicated_data['category_id']
    session.add(dep_obj)
    session.commit()
    replicated_data['sub_category_id'] = dep_obj.id
    return replicated_data
