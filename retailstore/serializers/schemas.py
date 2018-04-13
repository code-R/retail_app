from marshmallow import fields, Schema


class BaseSchema(Schema):
    id = fields.Integer()


class LocationSchema(BaseSchema):
    name = fields.String()


class DepartmentSchema(BaseSchema):
    name = fields.String()
    location_id = fields.Integer()
