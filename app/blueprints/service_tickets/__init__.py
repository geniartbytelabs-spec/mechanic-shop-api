from flask import Blueprint

service_tickets_bp = Blueprint('service_tickets', __name__, url_prefix='/service-tickets')

from app.blueprints.service_tickets import routes