from extensions import db


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    address = db.Column(db.String(200))

    service = db.Column(db.String(100))
    status = db.Column(db.String(30), default="Active")