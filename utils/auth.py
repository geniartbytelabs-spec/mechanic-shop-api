from jose import jwt, JWTError
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify

SECRET_KEY = "your-secret-key-change-this-in-production"
ALGORITHM = "HS256"


def encode_token(customer_id):
    payload = {
        "sub": str(customer_id),
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=1),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def encode_mechanic_token(mechanic_id):
    payload = {
        "sub": str(mechanic_id),
        "role": "mechanic",
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=1),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"error": "Token is missing"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            customer_id = int(data["sub"])
        except JWTError:
            return jsonify({"error": "Token is invalid or expired"}), 401

        return f(customer_id, *args, **kwargs)
    return decorated


def mechanic_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"error": "Token is missing"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            if data.get("role") != "mechanic":
                return jsonify({"error": "Mechanic access required"}), 403
            mechanic_id = int(data["sub"])
        except JWTError:
            return jsonify({"error": "Token is invalid or expired"}), 401

        return f(mechanic_id, *args, **kwargs)
    return decorated