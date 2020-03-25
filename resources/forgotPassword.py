import random
import string

from flask import request
from flask_restful import Resource

from model import db, ForgotPasswordStatus, WeConnectUsers


class ForgotPassword(Resource):
    def get(self):
        email_id = request.args["email"]
        if db.session().query(WeConnectUsers).filter_by(emailId=email_id).first():
            if db.session().query(ForgotPasswordStatus).filter_by(emailId=email_id).first():
                db.session().query(ForgotPasswordStatus).filter_by(emailId=email_id).delete()
            otp = ''.join(random.choice(string.digits) for _ in range(6))
            print(otp)
            db.create_all()
            key = ForgotPasswordStatus(email_id, otp)
            db.session.add(key)
            db.session.commit()
            return {"message" : "Otp Sent"}, 200
        else:
            return {"message" : "Email id not registered"}, 409