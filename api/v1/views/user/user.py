from v1.views import app_views
from werkzeug.utils import secure_filename
from flask import request, send_from_directory, current_app, send_file, jsonify
import os
from v1.views.user.models import Upload
from v1 import app, db
import dotenv
# import smtplib
from flask_jwt_extended import jwt_required
from uuid import uuid4

@app_views.route('/uploadfile', methods=['POST'])
def upload_file():
    """Endpoint to upload APK files with will return a unique id"""

    # .env management
    dotenv.load_dotenv(override=True)
    count = os.getenv('UPLOAD_NUMBER')
    num = int(os.getenv('UPLOAD_NUMBER')) + 1
    dotenv.set_key('.env', 'UPLOAD_NUMBER', str(num))

    if (request.method == 'POST'):
        path = None
        link = None
        # check if the post request has the file part
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return ("file empty")
            filename = secure_filename(file.filename)
            new_name = count + '.' + filename
            path = os.path.join(app.config['UPLOAD_FOLDER_FEEDBACK'], new_name)
            file.save(path)
            path = "http://localhost:5000/api/v1/download/" + new_name

        elif (request.form.get('url')):
            link = request.form.get('url')
        
        if (request.form.get("email")):
            email = request.form.get("email")
            upload = Upload(email=email, file_path=path, link=link, id= "Upload" + "." + str(uuid4()))
            db.session.add(upload)
            db.session.commit()
            return (jsonify({"id": upload.id}))
        return (jsonify({"error": "bad request"}), 400)


@app_views.route("/all_upload", methods=['GET'])
@jwt_required()
def all_upload():
    """Get all uploaded file"""
    uploads = Upload.query.all()
    new_list = []
    for upload in uploads:
        new_dict = upload.__dict__.copy()
        del new_dict["_sa_instance_state"]
        new_list.append(new_dict)
        del new_dict
    return (jsonify(new_list))


@app_views.route('/get_upload/<id>', methods=["GET"])
@jwt_required()
def get_upload(id):
    upload = Upload.query.filter_by(id=id).first()
    if upload == None:
        return (jsonify({"error": "not found"}))
    upload = upload.__dict__.copy()
    del upload['_sa_instance_state']
    return(jsonify(upload))


@app_views.route('/download/<filename>', methods=['GET'])
@jwt_required()
def download(filename):
    """TO download the apk file"""
    return send_from_directory(app.root_path[:-2] + 'file/feedback', filename, as_attachment=True)


# @app_views.route('/send_email', methods=['POST'])
# def send_email():
#     """route to send email"""
#     sender_email = "standard.forever123@gmail.com"
#     sender_password = "#!/usr/bin/bash"
#     # recipient_email = request.form['recipient_email']
#     # subject = request.form['subject']
#     # message = request.form['message']
#     recipient_email = "yusufkusimo12345@gmail.com"
#     subject = "Email"
#     message = "The right message"

#     try:
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()
#         server.login(sender_email, sender_password)

#         email_text = "From: {}\nTo: {}\nSubject: {}\n\n{}".format(sender_email, recipient_email, subject, message)
#         server.sendmail(sender_email, recipient_email, email_text)

#         return 'Email sent successfully!'
#     except Exception as e:
#         return 'Error: {}'.format(str(e))


