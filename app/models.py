from app.extensions import db

service_mechanic = db.Table(
    'service_mechanic',
    db.Column('ticket_id',   db.Integer, db.ForeignKey('service_tickets.id'), primary_key=True),
    db.Column('mechanic_id', db.Integer, db.ForeignKey('mechanics.id'),       primary_key=True)
)


class Customer(db.Model):
    __tablename__ = 'customers'

    id    = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(20))

    service_tickets = db.relationship('ServiceTicket', back_populates='customer')


class Mechanic(db.Model):
    __tablename__ = 'mechanics'

    id     = db.Column(db.Integer, primary_key=True)
    name   = db.Column(db.String(100), nullable=False)
    email  = db.Column(db.String(150), unique=True, nullable=False)
    phone  = db.Column(db.String(20))
    salary = db.Column(db.Float)

    service_tickets = db.relationship(
        'ServiceTicket',
        secondary=service_mechanic,
        back_populates='mechanics'
    )


class ServiceTicket(db.Model):
    __tablename__ = 'service_tickets'

    id           = db.Column(db.Integer, primary_key=True)
    vin          = db.Column(db.String(17), nullable=False)
    service_date = db.Column(db.Date, nullable=False)
    service_desc = db.Column(db.Text)
    customer_id  = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)

    customer  = db.relationship('Customer', back_populates='service_tickets')
    mechanics = db.relationship(
        'Mechanic',
        secondary=service_mechanic,
        back_populates='service_tickets'
    )