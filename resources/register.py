import hashlib
import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_restful import Resource
from flask import request
from model import db, WeConnectUsers, VerificationStatus
import re


class Register(Resource):
    @staticmethod
    def post():
        try:
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
                return {"response": "Missing Password"}, 422
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
                if db.session().query(VerificationStatus).filter_by(emailId=email_id).first():
                    db.session().query(VerificationStatus).filter_by(emailId=email_id).delete()
                key = VerificationStatus(email_id, verification_key)
                server = smtplib.SMTP('smtp.gmail.com:587')
                server.ehlo()
                server.starttls()
                message = MIMEMultipart()
                message['From'] = "ayush1641138@gmail.com"
                message['To'] = email_id
                message['Subject'] = 'Confirm your WeConnect Account'
                message.attach(MIMEText("Welcome to WeConnect. Click on the below link to activate your account.\nhttps://weconnect-insta.herokuapp.com/api/verifyEmail?key=" + verification_key + "&email=" + email_id, 'plain'))
                text = message.as_string()
                server.login("ayush1641138@gmail.com", "Ayushanand@16")
                server.sendmail("ayush1641138@gmail.com", email_id, text)
                server.quit()
                db.session.add(key)
                db.session.commit()
                return {"message": "User Created"}, 201
            else:
                return {"message" : "Email id is not in valid format"}, 422
        except:
            return {"message" : "Something went wrong"}, 500