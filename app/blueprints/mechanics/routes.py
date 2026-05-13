from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, func

from app.extensions import db
from app.models import Mechanic, service_mechanic
from app.blueprints.mechanics import mechanics_bp
from app.blueprints.mechanics.schemas import mechanic_schema, mechanics_schema, mechanic_login_schema
from utils.auth import encode_mechanic_token, mechanic_token_required


@mechanics_bp.route('/', methods=['POST'])
def create_mechanic():
    try:
        new_mechanic = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    try:
        db.session.add(new_mechanic)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "A mechanic with that email already exists"}), 400
    return mechanic_schema.jsonify(new_mechanic), 201


@mechanics_bp.route('/', methods=['GET'])
def get_mechanics():
    mechanics = db.session.execute(select(Mechanic)).scalars().all()
    return mechanics_schema.jsonify(mechanics), 200


@mechanics_bp.route('/login', methods=['POST'])
def mechanic_login():
    try:
        credentials = mechanic_login_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    mechanic = db.session.execute(
        select(Mechanic).where(Mechanic.email == credentials['email'])
    ).scalar_one_or_none()
    if not mechanic or mechanic.password != credentials['password']:
        return jsonify({"error": "Invalid email or password"}), 401
    token = encode_mechanic_token(mechanic.id)
    return jsonify({"token": token, "message": "Login successful"}), 200


@mechanics_bp.route('/most-worked', methods=['GET'])
def most_worked():
    results = db.session.execute(
        select(Mechanic, func.count(service_mechanic.c.ticket_id).label('ticket_count'))
        .outerjoin(service_mechanic, Mechanic.id == service_mechanic.c.mechanic_id)
        .group_by(Mechanic.id)
        .order_by(func.count(service_mechanic.c.ticket_id).desc())
    ).all()
    output = []
    for mechanic, count in results:
        data = mechanic_schema.dump(mechanic)
        data['ticket_count'] = count
        output.append(data)
    return jsonify(output), 200


@mechanics_bp.route('/<int:id>', methods=['PUT'])
@mechanic_token_required
def update_mechanic(mechanic_id, id):
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404
    try:
        updated_mechanic = mechanic_schema.load(
            request.json, instance=mechanic, partial=True
        )
    except ValidationError as e:
        return jsonify(e.messages), 400
    db.session.commit()
    return mechanic_schema.jsonify(updated_mechanic), 200


@mechanics_bp.route('/<int:id>', methods=['DELETE'])
@mechanic_token_required
def delete_mechanic(mechanic_id, id):
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"Mechanic {id} deleted successfully"}), 200
