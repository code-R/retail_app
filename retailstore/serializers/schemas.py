from marshmallow import fields, Schema


class BaseSchema(Schema):
    id = fields.Integer()


class LocationSchema(BaseSchema):
    name = fields.String(required=True)
    description = fields.String()
    created_at = fields.DateTime(attribute="created_at")

    def hiera_data(self, location):
        res = {
            'name': location.name,
            'children': []
        }

        departments = location.departments
        department_schema = DepartmentSchema()
        for department in departments:
            res['children'].append(
                department_schema.hiera_data(department))

        return res


class DepartmentSchema(BaseSchema):
    name = fields.String(required=True)
    description = fields.String()
    created_at = fields.DateTime(attribute="created_at")
    location_id = fields.Integer()

    def hiera_data(self, department):
        res = {
            'name': department.name,
            'children': []
        }

        categories = department.categories
        category_schema = CategorySchema()
        for category in categories:
            res['children'].append(
                category_schema.hiera_data(category))

        return res


class CategorySchema(BaseSchema):
    name = fields.String(required=True)
    description = fields.String()
    created_at = fields.DateTime(attribute="created_at")
    department_id = fields.Integer()

    def hiera_data(self, category):
        res = {
            'name': category.name,
            'children': []
        }

        sub_categories = category.sub_categories
        for sub_category in sub_categories:
            res['children'].append({
                "name": sub_category.name
            })

        return res


class SubCategorySchema(BaseSchema):
    name = fields.String(required=True)
    description = fields.String()
    created_at = fields.DateTime(attribute="created_at")
    category_id = fields.Integer()
