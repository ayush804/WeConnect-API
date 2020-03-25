import hashlib
import os
import random
import string

from flask_restful import Resource
from flask import request
from sendgrid import sendgrid, From, To, Content, Mail

from model import db, WeConnectUsers, VerificationStatus
import re


class Register(Resource):
    def post(self):
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        json_data = request.get_json(force=True)
        sex, name="", ""
        dob = None
        if not json_data:
            return {"message": "No input data provided"}, 400
        if "emailId" in json_data:
            email_id = json_data['emailId']
        else:
            return {"message" : "Missing Email id"}, 422
        if "password" in json_data:
            password = json_data['password']
            password = hashlib.md5(password.encode())
            password = password.hexdigest()
        else:
            return {"response": "Missing Password"}
        if "sex" in json_data:
            sex = json_data['sex']
        if "dob" in json_data:
            dob = json_data['dob']
        if "name" in json_data:
            name = json_data['name']
        if re.search(regex, email_id):
            if db.session().query(WeConnectUsers).filter_by(emailId=email_id).first():
                return {"message" : "User already exist"}, 409
            db.create_all()
            user = WeConnectUsers(email_id, password, sex, dob, name)
            db.session.add(user)
            verification_key = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase)
                                       for _ in range(50))
            db.create_all()
            key = VerificationStatus(email_id, verification_key)
            db.session.add(key)
            db.session.commit()
            sg = sendgrid.SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
            from_email = From("ayush804@gmail.com")
            subject = "Verify your email : WeConnect "
            to_email = To(email_id)
            content = Content("text/plain", verification_key)
            mail = Mail(from_email, to_email, subject, content)
            response = sg.send(mail)
            print(response.status_code)
            print(response.body)
            print(response.headers)
            return {"message": "User Created"}, 201
        else:
            return {"message" : "Email id is not in valid format"}