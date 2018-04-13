from marshmallow import fields, Schema


class BaseSchema(Schema):
    id = fields.Integer()


class LocationSchema(BaseSchema):
    name = fields.String(required=True)
    description = fields.String()
    created_at = fields.DateTime(attribute="created_at")


class DepartmentSchema(BaseSchema):
    name = fields.String(required=True)
    description = fields.String()
    created_at = fields.DateTime(attribute="created_at")
    location_id = fields.Integer()
