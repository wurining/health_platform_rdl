from applications.extensions import ma
from marshmallow import fields


class LogOutSchema(ma.Schema):
    id = fields.Integer()
    method = fields.Str()
    uid = fields.Str()
    url = fields.Str()
    desc = fields.Str()
    ip = fields.Str()
    user_agent = fields.Str()
    username = fields.Str()
    browser = fields.Str()
    os = fields.Str()
    location = fields.Str()
    success = fields.Bool()
    operation_type = fields.Str()
    module_name = fields.Str()
    create_time = fields.DateTime()
