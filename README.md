# Mechanic Shop API

A REST API for managing a mechanic shop built with Flask, SQLAlchemy, and Marshmallow.

## Features
- Customer management (CRUD) with JWT authentication
- Mechanic management (CRUD) with JWT authentication
- Service ticket management with inventory tracking
- Rate limiting and caching
- Token-based authentication for protected routes
- Inventory management (CRUD)
- Pagination on customer listing
- Mechanics ranked by number of tickets worked

## Tech Stack
- Python 3.11
- Flask
- Flask-SQLAlchemy
- Flask-Marshmallow
- Flask-Limiter
- Flask-Caching
- python-jose (JWT)
- SQLite

## Setup Instructions

1. Clone the repository
   git clone <your-repo-url>
   cd mechanic-shop-api

2. Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate

3. Install dependencies
   pip install flask flask-sqlalchemy flask-marshmallow marshmallow-sqlalchemy flask-limiter flask-caching python-jose

4. Run the server
   python run.py

5. Server runs at http://127.0.0.1:5001

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | /customers/ | Create a customer | No |
| GET | /customers/ | Get all customers (paginated, cached) | No |
| POST | /customers/login | Customer login, returns JWT token | No |
| GET | /customers/my-tickets | Get current customer's tickets | Customer Token |
| PUT | /customers/<id> | Update a customer | Customer Token |
| DELETE | /customers/<id> | Delete a customer | Customer Token |
| POST | /mechanics/ | Create a mechanic | No |
| GET | /mechanics/ | Get all mechanics | No |
| POST | /mechanics/login | Mechanic login, returns JWT token | No |
| GET | /mechanics/most-worked | Get mechanics ranked by tickets worked | No |
| PUT | /mechanics/<id> | Update a mechanic | Mechanic Token |
| DELETE | /mechanics/<id> | Delete a mechanic | Mechanic Token |
| POST | /service-tickets/ | Create a service ticket | No |
| GET | /service-tickets/ | Get all service tickets | No |
| PUT | /service-tickets/<id>/edit | Add/remove mechanics from ticket | No |
| POST | /service-tickets/<id>/add-part | Add inventory part to ticket | No |
| POST | /inventory/ | Create an inventory part | No |
| GET | /inventory/ | Get all inventory parts | No |
| PUT | /inventory/<id> | Update an inventory part | No |
| DELETE | /inventory/<id> | Delete an inventory part | No |

## Authentication

This API uses JWT (JSON Web Token) authentication.

To access protected routes:
1. Login via POST /customers/login or POST /mechanics/login
2. Copy the token from the response
3. Add to request headers: Authorization: Bearer <token>