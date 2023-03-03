from v1 import app, db
from v1.views.admin.models import FeedBack, Review, ReviewComment, ReviewImages
from v1.views.user.models import Upload
from v1.views.staff.models import Staff
from v1.views import app_views
from sqlalchemy.exc import IntegrityError
from flask import request, jsonify
import uuid
import dotenv
import os
from flask_jwt_extended import get_jwt
from flask_jwt_extended import jwt_required
from datetime import datetime
from werkzeug.utils import secure_filename


@app_views.route('/feedback', methods=['POST'])
@jwt_required()
def feedback():
    """Method to create a feedback message"""
    if request.method == 'POST':
        id = "Feedback" + '.' + str(uuid.uuid4())
        ticket_id = request.json.get('ticket_id')
        # email = request.json.get('email')
        types = request.json.get('types')
        link = request.json.get('link')
        apk_id = request.json.get('apk_id')
        status = request.json.get('status')
        assigned_to = request.json.get('assigned_to')
        staff_id = request.json.get("staff_id")
        
        
        status_code = ['pending', 'active', 'completed']

        if (status.lower() not in status_code):
            return(jsonify({"error": "wrong status"}), 400)

        upload = Upload.query.filter_by(id=apk_id).first()
        if (upload == None):
            return (jsonify({"error": "wrong id"}), 400)

        new_feedback = FeedBack(ticket_id=ticket_id, types=types, id=id, staff_id=staff_id,
                                link=link, apk_id=apk_id, status=status, assigned_to=assigned_to)

        new_dict = new_feedback.__dict__.copy()
        if (new_dict["_sa_instance_state"]):
            del new_dict["_sa_instance_state"]

        db.session.add(new_feedback)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return (jsonify({"error": "wrong input"}), 400)
        return (jsonify(new_dict), 201)
        

@app_views.route('/get_feedback', methods=['GET'])
@jwt_required()
def get_feedback():
    """ Endpoint to get all feedback requests"""
    new_list = []
    
    feedbacks = FeedBack.query.all()

    """Get list of all feedback"""
    for feedback in feedbacks:
        parent_dict = {"Feedback": {}, "User_upload": {}, "Reviews": {}}
        feedback_dict = feedback.__dict__.copy()

        """Get List of all reviews of a particular feedback"""    
        reviews = Review.query.filter(Review.feedback_id==feedback.id).all()
        dic = []

        """Get all uploaded reviews images and comment of the feedback"""
        for review in reviews:
            if (len(review.review_comment) > 0):
                new_comm = review.review_comment[0].__dict__.copy()
                del new_comm['_sa_instance_state']
                dic.append(new_comm)
                del new_comm

            elif (len(review.review_image) > 0):
                new_image = review.review_image[0].__dict__.copy()
                del new_image['_sa_instance_state']
                dic.append(new_image)
                del new_image
            
        parent_dict["Reviews"] = dic
       
        """Get the File which to make feedback on"""
        if (feedback.upload is not None):
            user_upload = feedback.upload.__dict__.copy()
            del user_upload['_sa_instance_state']
            parent_dict["User_upload"] = user_upload
            del user_upload

        del feedback_dict['_sa_instance_state']
        parent_dict["Feedback"] = feedback_dict
    

        new_list.append(parent_dict)

        del feedback_dict
        del parent_dict

    return (jsonify(new_list), 200)



@app_views.route("/get_feedback_id/<id>", methods=['GET'])
@jwt_required()
def get_feedback_id(id):
    """ Endpoint to get a feedback request by id """
    new_list = []

    feedback = FeedBack.query.filter_by(id=id).first()
    if (feedback is None):
        return (jsonify({"error": "feedback not found"}), 400)

    parent_dict = {"Feedback": {}, "User_upload": {}, "Reviews": {}}
    feedback_dict = feedback.__dict__.copy()

    """Get List of all reviews of a particular feedback"""    
    reviews = Review.query.filter(Review.feedback_id==feedback.id).all()
    dic = []

    """Get all uploaded reviews images and comment of the feedback"""
    for review in reviews:
        if (len(review.review_comment) > 0):
            new_comm = review.review_comment[0].__dict__.copy()
            del new_comm['_sa_instance_state']
            dic.append(new_comm)
            del new_comm

        elif (len(review.review_image) > 0):
            new_image = review.review_image[0].__dict__.copy()
            del new_image['_sa_instance_state']
            dic.append(new_image)
            del new_image
        
    parent_dict["Reviews"] = dic
    
    """Get the File which to make feedback on"""
    if (feedback.upload is not None):
        user_upload = feedback.upload.__dict__.copy()
        del user_upload['_sa_instance_state']
        parent_dict["User_upload"] = user_upload
        del user_upload

    del feedback_dict['_sa_instance_state']
    parent_dict["Feedback"] = feedback_dict


    new_list.append(parent_dict)

    del feedback_dict
    del parent_dict

    return (jsonify(new_list), 200)


@app_views.route("/cloose_feedback/<id>", methods=['GET'])
@jwt_required()
def cloose_feedback(id):
    """Endpoint to close a feedback request"""
    feedback = FeedBack.query.filter_by(id=id).first()

    if (feedback != None and feedback.status != "completed"):
        feedback.status = 'completed'
        new = feedback.__dict__.copy()
        del new['_sa_instance_state']
        db.session.commit()
        return (jsonify({"succes": "ok", "feedback": new}))
    return (jsonify({"error": "feedback not found or already closed"}), 400)


@app_views.route("/assign_feedback", methods=["POST"])
@jwt_required()
def assign_feedback():
    """ Endpoint to self-assign a feedback request to the logged in user"""
    if request.method == "POST":
        staff_id = request.json.get("staff_id")
        feedback_id = request.json.get("feedback_id")

        if (staff_id == None or feedback_id == None):
            return (jsonify({"error": "user or feedback not found"}, 400))

        staff = Staff.query.filter_by(id=staff_id).first()
        feedback = FeedBack.query.filter_by(id=feedback_id).first()
        
        if (staff == None or feedback == None):
            return (jsonify({"error": "user or feedback not found"}), 400)
        
        if (feedback.status == 'active' or feedback.status == 'completed'):
            return (jsonify({"error": "feedback assigned to someone or closed!"}), 400)
        
        feedback.status = "active"
        feedback.assigned_to = staff.email
        feedback.staff_id = staff.id
        feedback.updated_at = datetime.utcnow()
        db.session.commit()
        return (jsonify({"success": "ok"}))
        

@app_views.route("/unassigned_feedback", methods=["POST"])
def unassigned_feedback():
    """Endpoint to unassign a feedback request from the logged in user"""
    if request.method == "POST":
        staff_id = request.json.get("staff_id")
        feedback_id = request.json.get("feedback_id")

        if (staff_id == None or feedback_id == None):
            return (jsonify({"error": "user or feedback not found"}), 400)

        staff = Staff.query.filter_by(id=staff_id).first()
        feedback = FeedBack.query.filter_by(id=feedback_id).first()
        
        if (staff == None or feedback == None):
            return (jsonify({"error": "user or feedback not found"}), 400)
        
        if (feedback.staff == None or staff_id != feedback.staff.id  or feedback.status == 'completed'):
            return (jsonify({"error": "feedback assigned to someone or closed!"}), 400)

        feedback.status = "pending"
        feedback.staff_id = None
        db.session.commit()

        return (jsonify({"success": "ok"}))


@app_views.route("/all_assign_feedback/<id>")
@jwt_required()
def all_assign_feedback(id):
    staff = Staff.query.filter_by(id=id).first()
    if (staff == None):
        return (jsonify({"error": "user not found"}), 400)

    new_list = []
    """Get list of all feedback"""
    for feedback in staff.feed_back:
        parent_dict = {"Feedback": {}, "User_upload": {}, "Reviews": {}}
        feedback_dict = feedback.__dict__.copy()

        """Get List of all reviews of a particular feedback"""    
        reviews = Review.query.filter(Review.feedback_id==feedback.id).all()
        dic = []

        """Get all uploaded reviews images and comment of the feedback"""
        for review in reviews:
            if (len(review.review_comment) > 0):
                new_comm = review.review_comment[0].__dict__.copy()
                del new_comm['_sa_instance_state']
                dic.append(new_comm)
                del new_comm

            elif (len(review.review_image) > 0):
                new_image = review.review_image[0].__dict__.copy()
                del new_image['_sa_instance_state']
                dic.append(new_image)
                del new_image
            
        parent_dict["Reviews"] = dic
       
        """Get the File which to make feedback on"""
        if (feedback.upload is not None):
            user_upload = feedback.upload.__dict__.copy()
            del user_upload['_sa_instance_state']
            parent_dict["User_upload"] = user_upload
            del user_upload

        del feedback_dict['_sa_instance_state']
        parent_dict["Feedback"] = feedback_dict
    

        new_list.append(parent_dict)

        del feedback_dict
        del parent_dict

    return (jsonify(new_list), 200)


@app_views.route("/add_review_comm", methods=['POST'])
@jwt_required()
def add_review_comm():
    """Endpoint to add review to a feedback request"""

    if request.method == 'POST':
        staff_id = request.json.get("staff_id")
        feedback_id = request.json.get("feedback_id")
        comment = request.json.get("comment")

        if (staff_id == None or feedback_id == None):
            return (jsonify({"error": "user or feedback not found"}), 400)

        staff = Staff.query.filter_by(id=staff_id).first()
        feedback = FeedBack.query.filter_by(id=feedback_id).first()
        
        if (staff == None or feedback == None):
            return (jsonify({"error": "user or feedback not found"}), 400)
        
        if (feedback.staff == None or staff_id != feedback.staff.id):
            return (jsonify({"error": "feedback assigned to someone or closed!"}), 400)
        
        if (comment is not None):
            new_review = Review(feedback_id=feedback_id, id="Review" + "." + str(uuid.uuid4()))
            db.session.add(new_review)
            new_comment = ReviewComment(review_id=new_review.id, id="ReviewComment" + "." + str(uuid.uuid4()), comment=comment)
            db.session.add(new_comment)
            db.session.commit()
            return (jsonify({"success": "ok"}), 201)
    return (jsonify({"error": "Nothing to add"}), 400)
            

@app_views.route("/add_review_img", methods=['POST'])
@jwt_required()
def add_review_img():
    dotenv.load_dotenv(override=True)
    count = os.getenv('REVIEW')
    num = int(os.getenv('REVIEW')) + 1
    dotenv.set_key('.env', 'REVIEW', str(num))

    staff_id = request.form.get("staff_id")
    feedback_id = request.form.get("feedback_id")

    if (staff_id == None or feedback_id == None):
            return (jsonify({"error": "user or feedback not found"}), 400)

    staff = Staff.query.filter_by(id=staff_id).first()
    feedback = FeedBack.query.filter_by(id=feedback_id).first()
    
    if (staff == None or feedback == None):
        return (jsonify({"error": "user or feedback not found"}), 400)
    
    if (feedback.staff == None or staff_id != feedback.staff.id):
        return (jsonify({"error": "feedback assigned to someone or closed!"}), 400)

    path = ''
    # check if the post request has the file part
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            filename = secure_filename(file.filename)
            new_name = count + '.' + filename
            path = os.path.join(app.config['UPLOAD_FOLDER_REVIEW'], new_name)
            file.save(path)
            path = "http://localhost:5000/api/v1/download/" + new_name

            new_review = Review(feedback_id=feedback_id, id="Review" + "." + str(uuid.uuid4()))
            db.session.add(new_review)
            new_image = ReviewImages(review_id=new_review.id, id="ReviewImage" + "." + str(uuid.uuid4()), image=path)
            db.session.add(new_image)
            db.session.commit()
            return (jsonify({"success": "ok"}), 201)
    return (jsonify({"error": "Nothing to add"}), 400)


# @app_views.route("/update_review", methods=['PUT'])
# def update_review():
#     """Endpoint to update review to a feedback request"""
#     pass



"""======admins======"""
# @app_views.route("/delete_review", methods=['DELETE'])
# def delete_review():
#     """Endpoint to delete review to a feedback request"""
#     pass


# @app_views.route("/delete_feedback/<id>", methods=['DELETE'])
# def delete_feedback(id):
#     """Endpoint to delete a feedback request"""
#     feedback = FeedBack.query.filter_by(id=id).first()
#     if feedback == None:
#         return jsonify({"error": "feedback not found"}, 400)
#     db.session.delete(feedback)
#     db.session.commit()
#     return (jsonify({"success": "ok"}))
    


# @app_views.route("/feedback_status/<id>", methods=['PUT'])
# @jwt_required()
# def feedback_status(id):
#     """Endpoint to change feedback status for all user"""
#     claims = get_jwt()
#     if claims['user'] != "admin":
#         return (jsonify({"error": "unauthorized"}), 401)
#     status = request.json.get("status")

#     if (id == None or status == None):
#         return (jsonify({"error": "id or status can't be null"}), 400)
#     feedback = FeedBack.query.filter_by(id=id).first()
#     if (feedback == None):
#         return (jsonify({"error": "feedback not found"}), 400)
#     status_code = ['pending', 'active', 'completed']
#     if status.lower() not in status_code:
#         return(jsonify({"error": "wrong status"}), 400)
#     feedback.status = status
#     if (status == 'pending')
#     feedback.
#     db.session.commit()
#     return (jsonify({"sucess": "ok"}))
