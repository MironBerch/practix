from marshmallow import Schema, fields


class SignUpSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, min_length=6)


class SignInSchema(SignUpSchema):
    ...


class ConfirmCodeSchema(Schema):
    code = fields.String(required=True, min_length=6, max_length=6)


class PasswordChangeSchema(Schema):
    old_password = fields.String(required=True, min_length=6)
    new_password = fields.String(required=True, min_length=6)


class EmailSchema(Schema):
    email = fields.Email(required=True)
