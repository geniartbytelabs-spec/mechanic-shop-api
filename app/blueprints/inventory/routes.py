from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select

from app.extensions import db
from app.models import Inventory
from app.blueprints.inventory import inventory_bp
from app.blueprints.inventory.schemas import inventory_schema, inventories_schema


@inventory_bp.route('/', methods=['POST'])
def create_part():
    try:
        new_part = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    db.session.add(new_part)
    db.session.commit()
    return inventory_schema.jsonify(new_part), 201


@inventory_bp.route('/', methods=['GET'])
def get_inventory():
    parts = db.session.execute(select(Inventory)).scalars().all()
    return inventories_schema.jsonify(parts), 200


@inventory_bp.route('/<int:id>', methods=['PUT'])
def update_part(id):
    part = db.session.get(Inventory, id)
    if not part:
        return jsonify({"error": "Part not found"}), 404

    try:
        updated_part = inventory_schema.load(
            request.json,
            instance=part,
            partial=True
        )
    except ValidationError as e:
        return jsonify(e.messages), 400

    db.session.commit()
    return inventory_schema.jsonify(updated_part), 200


@inventory_bp.route('/<int:id>', methods=['DELETE'])
def delete_part(id):
    part = db.session.get(Inventory, id)
    if not part:
        return jsonify({"error": "Part not found"}), 404

    db.session.delete(part)
    db.session.commit()
    return jsonify({"message": f"Part {id} deleted successfully"}), 200