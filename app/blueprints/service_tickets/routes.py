from flask import request, jsonify
from marshmallow import ValidationError
from app.extensions import db
from app.models import ServiceTicket, Mechanic, Inventory
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


@service_tickets_bp.route('/<int:ticket_id>/edit', methods=['PUT'])
def edit_ticket_mechanics(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404

    data       = request.json
    add_ids    = data.get('add_ids', [])
    remove_ids = data.get('remove_ids', [])

    for mechanic_id in add_ids:
        mechanic = db.session.get(Mechanic, mechanic_id)
        if mechanic and mechanic not in ticket.mechanics:
            ticket.mechanics.append(mechanic)

    for mechanic_id in remove_ids:
        mechanic = db.session.get(Mechanic, mechanic_id)
        if mechanic and mechanic in ticket.mechanics:
            ticket.mechanics.remove(mechanic)

    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200


@service_tickets_bp.route('/<int:ticket_id>/add-part', methods=['POST'])
def add_part_to_ticket(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404

    inventory_id = request.json.get('inventory_id')
    part = db.session.get(Inventory, inventory_id)
    if not part:
        return jsonify({"error": "Inventory item not found"}), 404

    if part not in ticket.inventory_items:
        ticket.inventory_items.append(part)
        db.session.commit()

    return service_ticket_schema.jsonify(ticket), 200