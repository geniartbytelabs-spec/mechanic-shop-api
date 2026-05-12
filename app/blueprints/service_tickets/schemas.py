import marshmallow as marsh
from app.extensions import ma
from app.models import ServiceTicket
from app.blueprints.mechanics.schemas import MechanicSchema


class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        load_instance = True
        include_fk = True

    mechanics = marsh.fields.Nested(MechanicSchema, many=True, dump_only=True)


service_ticket_schema  = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)