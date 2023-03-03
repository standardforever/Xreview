from v1 import app, db
from flask import jsonify, request
from v1.views.staff.models import Staff
from v1.views import app_views
import uuid
from sqlalchemy.exc import IntegrityError
from passlib.hash import sha256_crypt
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import jwt_required


@app_views.route('/create_staff', methods=["POST"])
@jwt_required()
def create_staff():
    """End poin to create a saff"""
    claims = get_jwt()
    if claims['user'] != "admin":
        return (jsonify({"error": "unauthorized"}), 401)
    if request.method == 'POST':
        id = "Staff" + "." + str(uuid.uuid4())
        first_name = request.json.get("first_name")
        last_name = request.json.get("last_name")
        email = request.json.get("email")
        address = request.json.get("address")
        phone = request.json.get("phone")
        role = request.json.get("role")
        password = request.json.get("password")

        if (first_name == None or last_name == None or email == None or address == None):
            return (jsonify({"error": "Bad request"}), 400)
        
        if (phone == None or role == None or password == None):
            return (jsonify({"error": "Bad request"}), 400)

        password = sha256_crypt.encrypt(password)


        roles = ['admin', 'staff']
        if role.lower() not in roles:
            return (jsonify({"error": "role error"}), 400)
        staff = Staff(first_name=first_name, last_name=last_name, email=email,id=id,
                      address=address, phone=phone, role=role, password=password)
        db.session.add(staff)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return (jsonify({"errro": "Invalid input"}), 400)
        return (jsonify({"success": "ok", "id": staff.id}), 201)


@app_views.route('/get_staff', methods=['GET'])
@jwt_required()
def get_staff():
    """ Endpoint to get all staff"""
    new_list = []
    staffs = Staff.query.all()
    
    for staff in staffs:
        new_dict = staff.__dict__.copy()
        del new_dict["password"]
        if '_sa_instance_state' in new_dict:
            del new_dict['_sa_instance_state']
        new_list.append(new_dict)
        del new_dict
    return (jsonify(new_list), 200)


@app_views.route("/get_staff_id/<id>", methods=['GET'])
@jwt_required()
def get_staff_id(id):
    """ Endpoint to get a   staff request by id """
    staff = Staff.query.filter_by(id=id).first()
    if  staff == None:
        return (jsonify({"error": "user not found"}))
    new_dict =  staff.__dict__.copy()
    # del new_dict["password"]
    if '_sa_instance_state' in new_dict:
        del new_dict['_sa_instance_state'] 
        del new_dict['password']
    return(jsonify(new_dict))


@app_views.route('/update_staff/<id>', methods=['PUT'])
@jwt_required()
def update_staff(id):
    if request.method == 'PUT':
        staff = Staff.query.filter_by(id=id).first()
        if (staff == None):
            return (jsonify({"error": "User not found"}))
        if (request.json.get("first_name") != None):
            staff.first_name = request.json.get("first_name")
        if (request.json.get("last_name") != None):
            staff.last_name = request.json.get("last_name")
        if (request.json.get("email") != None):
            staff.email = request.json.get("email")
        if (request.json.get("address") != None):
            staff.address = request.json.get("address")
        if (request.json.get("phone") != None):
            staff.phone = request.json.get("phone")
        if (request.json.get("role") != None):
            staff.role = request.json.get("role")
        if (request.json.get("old_password") != None and request.json.get("password")):
            if (sha256_crypt.verify(request.json.get("old_password"), staff.password)):
                staff.password = sha256_crypt.encrypt(request.json.get("password"))
        new_dict = staff.__dict__.copy()
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return (jsonify({"errro": "Invalid input"}), 400)
        del new_dict['_sa_instance_state']
        del new_dict['password']
        return (jsonify(new_dict))


@app_views.route("/login", methods=['POST'])
def login():
    """Endpoint for login"""
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    staff = Staff.query.filter_by(email=email).first()
    if (staff == None or password == None):
        return (jsonify({"error": "password or email not found"}), 400)
    if (sha256_crypt.verify(password, staff.password)):
        # custom claims or override default claims in the JWT.
        additional_claims = {"user": staff.role}
        access_token = create_access_token(email, additional_claims=additional_claims)
        return jsonify(access_token=access_token)
    return (jsonify({"error": "password or email not found"}), 400)



""" ===== Admins === """

@app_views.route('/delete_staff/<id>', methods=['DELETE'])
@jwt_required()
def delete_staff(id):
    claims = get_jwt()
    if claims["user"] != "admin":
        return (jsonify({"error": "unauthorized"}), 401)
    staff = Staff.query.filter_by(id=id).first()
    if (staff != None):
        db.session.delete(staff)
        db.session.commit()
        return (jsonify({"success": "ok"}))
    return (jsonify({"error": "user not found"}))

        
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)