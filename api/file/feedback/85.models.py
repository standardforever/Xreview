from v1 import db, app
import uuid
from datetime import datetime


class Upload(db.Model):
    """Model for uploading file"""
    id = db.Column(db.String(80), nullable=False, primary_key=True)
    email = db.Column(db.String(80), nullable=False)
    updated_at = db.Column(db.String(120), nullable=False, default=datetime.utcnow())
    file_path= db.Column(db.String(200), nullable=True, unique=True)
    link = db.Column(db.String(200), nullable=True)
    feed_back = db.relationship("FeedBack", backref="upload", cascade="all, delete")

with app.app_context():   # all database operations under with
    db.create_all() 