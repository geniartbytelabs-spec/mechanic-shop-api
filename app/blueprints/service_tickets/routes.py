from flask import request, jsonify
from marshmallow import ValidationError

from app.extensions import db
from app.models import ServiceTicket, Mechanic
from app.blueprints.service_tickets import service_tickets_bp
from app.blueprints.service_tickets.schemas import service_ticket_schema, service_tickets_schema


@service_tickets_bp.route('/', methods=['POST'])
def create_ticket():
    try:
        new_ticket = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    db.session.add(new_ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(new_ticket), 201


@service_tickets_bp.route('/', methods=['GET'])
def get_tickets():
    tickets = db.session.execute(db.select(ServiceTicket)).scalars().all()
    return service_tickets_schema.jsonify(tickets), 200


@service_tickets_bp.route('/<int:ticket_id>/assign-mechanic/<int:mechanic_id>', methods=['PUT'])
def assign_mechanic(ticket_id, mechanic_id):
    ticket   = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not ticket:
        return jsonify({"error": f"Service ticket {ticket_id} not found"}), 404
    if not mechanic:
        return jsonify({"error": f"Mechanic {mechanic_id} not found"}), 404

    if mechanic in ticket.mechanics:
        return jsonify({"message": "Mechanic is already assigned to this ticket"}), 400

    ticket.mechanics.append(mechanic)
    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200


@service_tickets_bp.route('/<int:ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    ticket   = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not ticket:
        return jsonify({"error": f"Service ticket {ticket_id} not found"}), 404
    if not mechanic:
        return jsonify({"error": f"Mechanic {mechanic_id} not found"}), 404

    if mechanic not in ticket.mechanics:
        return jsonify({"message": "Mechanic is not assigned to this ticket"}), 400

    ticket.mechanics.remove(mechanic)
    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200