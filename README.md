# Mechanic Shop API

A REST API for managing a mechanic shop built with Flask, SQLAlchemy, and Marshmallow.

## Features
- Customer management (CRUD)
- Mechanic management (CRUD)
- Service ticket management
- Assign and remove mechanics from service tickets

## Tech Stack
- Python 3.11
- Flask
- Flask-SQLAlchemy
- Flask-Marshmallow
- SQLite

## Setup Instructions

1. Clone the repository
   git clone <your-repo-url>
   cd mechanic-shop-api

2. Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate

3. Install dependencies
   pip install flask flask-sqlalchemy flask-marshmallow marshmallow-sqlalchemy

4. Run the server
   python run.py

5. Server runs at http://127.0.0.1:5000

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /customers/ | Create a customer |
| GET | /customers/ | Get all customers |
| PUT | /customers/<id> | Update a customer |
| DELETE | /customers/<id> | Delete a customer |
| POST | /mechanics/ | Create a mechanic |
| GET | /mechanics/ | Get all mechanics |
| PUT | /mechanics/<id> | Update a mechanic |
| DELETE | /mechanics/<id> | Delete a mechanic |
| POST | /service-tickets/ | Create a service ticket |
| GET | /service-tickets/ | Get all service tickets |
| PUT | /service-tickets/<ticket_id>/assign-mechanic/<mechanic_id> | Assign mechanic to ticket |
| PUT | /service-tickets/<ticket_id>/remove-mechanic/<mechanic_id> | Remove mechanic from ticket |