import hashlib

from flask import request
from flask_restful import Resource

from model import ForgotPasswordStatus, db, WeConnectUsers


class ChangePassword(Resource):
    def change_password(self, email_id, json):
        user = db.session().query(WeConnectUsers).filter_by(emailId=email_id).first()
        old_password = json["oldPassword"]
        old_password = hashlib.md5(old_password.encode())
        old_password = old_password.hexdigest()
        if user.__dict__['password'] != old_password:
            return {"message" : "Incorrect Old Password"}
        else:
            user = db.session().query(WeConnectUsers).filter_by(emailId=email_id).first()
            password = json["newPassword"]
            new_password = hashlib.md5(password.encode())
            new_password = new_password.hexdigest()
            user.password = new_password
            db.session().commit()

    def reset_password(self, email_id, json):
        user = db.session().query(WeConnectUsers).filter_by(emailId=email_id).first()
        password = json["newPassword"]
        new_password = hashlib.md5(password.encode())
        new_password = new_password.hexdigest()
        user.password = new_password
        db.session().commit()

    def post(self):
        if "email" in request.args and "otp" in request.args:
            if db.session().query(ForgotPasswordStatus).filter_by(emailId=request.args["email"], otp = request.args["otp"]).first():
                db.session().query(ForgotPasswordStatus).filter_by(emailId=request.args["email"]).delete()
                self.reset_password(request.args["email"], request.get_json(force=True))
                db.session().commit()
            else:
                return {"message" : "Invalid OTP"}
        else:
            self.change_password(request.args["email"], request.get_json(force=True))
        return {"message": "Password Change Successful"}