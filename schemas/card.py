from marshmallow import Schema, fields, validate

languages = ["en", "pt", "es"]


class Content(Schema):
    word = fields.Str(required=True)
    language = fields.Str(validate=validate.OneOf(languages), required=True)
    translation_language = fields.Str(validate=validate.OneOf(languages), required=True)
