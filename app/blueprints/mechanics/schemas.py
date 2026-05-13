from app.extensions import ma
from app.models import Mechanic
from marshmallow import fields


class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        load_instance = True

    password = fields.String(load_only=True, required=True)


class MechanicLoginSchema(ma.Schema):
    email    = fields.Email(required=True)
    password = fields.String(required=True)


mechanic_schema       = MechanicSchema()
mechanics_schema      = MechanicSchema(many=True)
mechanic_login_schema = MechanicLoginSchema()