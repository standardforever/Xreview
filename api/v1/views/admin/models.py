from v1 import db, app
from datetime import datetime



"""Mode for feedback request"""
class FeedBack(db.Model):
    id = db.Column(db.String(80), primary_key = True)
    ticket_id = db.Column(db.String(80), nullable=False) # is a foreign key
    # email = db.Column(db.String(80), nullable=False, unique=True)
    types = db.Column(db.String(120), nullable=False)
    link = db.Column(db.String(120), nullable=True, default=None)
    apk_id = db.Column(db.String(120), db.ForeignKey("upload.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    assigned_to = db.Column(db.String(80), default=None, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())
    staff_id = db.Column(db.String(80), db.ForeignKey("staff.id"), nullable=True, default=None)

    review = db.relationship("Review", backref="feedback", cascade="all, delete")
   

class Review(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    feedback_id = db.Column(db.String(80), db.ForeignKey("feed_back.id"), nullable=False)
    
    review_comment = db.relationship("ReviewComment", backref="review", cascade="all, delete")
    review_image = db.relationship("ReviewImages", backref="review", cascade="all, delete")


class ReviewComment(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    comment = db.Column(db.Text, nullable=True, default=None)
    review_id = db.Column(db.String(80), db.ForeignKey("review.id"), nullable=True)


class ReviewImages(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    image = db.Column(db.String(120), nullable=True, default=None)
    review_id = db.Column(db.String(80), db.ForeignKey("review.id"), nullable=True)


with app.app_context():
    db.create_all()