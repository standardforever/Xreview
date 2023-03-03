from v1 import db, app

class Staff(db.Model):
    id = db.Column(db.String(80), nullable=False, unique=True, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    address = db.Column(db.String, nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    feed_back = db.relationship("FeedBack", backref="staff", lazy=True)

with app.app_context():
    db.create_all()