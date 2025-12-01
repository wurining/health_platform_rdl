from applications.extensions import ma
from marshmallow import fields


class UpdateLogOutSchema(ma.Schema):
    id = fields.Str(attribute="id")
    title = fields.Str(attribute="title")
    content = fields.Str(attribute="content")
    version = fields.Str(attribute="version")
    updateType = fields.Str(attribute="update_type")
    creator = fields.Str(attribute="creator")
    modifier = fields.Str(attribute="modifier")
    createTime = fields.Str(attribute="create_time")
    updateTime = fields.Str(attribute="update_time")

