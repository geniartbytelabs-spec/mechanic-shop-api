from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from app.extensions import db, limiter, cache
from app.models import Customer, ServiceTicket
from app.blueprints.customers import customers_bp
from app.blueprints.customers.schemas import customer_schema, customers_schema, login_schema
from utils.auth import encode_token, token_required


@customers_bp.route('/', methods=['POST'])
def create_customer():
    try:
        new_customer = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    try:
        db.session.add(new_customer)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email already exists"}), 400

    return customer_schema.jsonify(new_customer), 201


@customers_bp.route('/', methods=['GET'])
@cache.cached(timeout=60)
def get_customers():
    page     = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query      = select(Customer)
    pagination = db.paginate(query, page=page, per_page=per_page)

    return jsonify({
        "customers": customers_schema.dump(pagination.items),
        "total":     pagination.total,
        "page":      pagination.page,
        "pages":     pagination.pages,
        "per_page":  pagination.per_page,
    }), 200


@customers_bp.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    try:
        credentials = login_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    customer = db.session.execute(
        select(Customer).where(Customer.email == credentials['email'])
    ).scalar_one_or_none()

    if not customer or customer.password != credentials['password']:
        return jsonify({"error": "Invalid email or password"}), 401

    token = encode_token(customer.id)
    return jsonify({"token": token, "message": "Login successful"}), 200


@customers_bp.route('/my-tickets', methods=['GET'])
@token_required
def my_tickets(customer_id):
    tickets = db.session.execute(
        select(ServiceTicket).where(ServiceTicket.customer_id == customer_id)
    ).scalars().all()

    from app.blueprints.service_tickets.schemas import service_tickets_schema
    return service_tickets_schema.jsonify(tickets), 200


@customers_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_customer(customer_id, id):
    if customer_id != id:
        return jsonify({"error": "Unauthorized"}), 403

    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    try:
        updated_customer = customer_schema.load(
            request.json,
            instance=customer,
            partial=True
        )
    except ValidationError as e:
        return jsonify(e.messages), 400

    db.session.commit()
    return customer_schema.jsonify(updated_customer), 200


@customers_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_customer(customer_id, id):
    if customer_id != id:
        return jsonify({"error": "Unauthorized"}), 403

    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Customer {id} deleted successfully"}), 200