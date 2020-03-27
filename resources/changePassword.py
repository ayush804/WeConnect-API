import hashlib
from flask import request
from flask_restful import Resource
from model import ForgotPasswordStatus, db, WeConnectUsers


class ChangePassword(Resource):
    @staticmethod
    def change_password(self, email_id, json):
        user = db.session().query(WeConnectUsers).filter_by(emailId=email_id).first()
        old_password = json["oldPassword"]
        old_password = hashlib.md5(old_password.encode())
        old_password = old_password.hexdigest()
        if user.__dict__['password'] != old_password:
            return {"message": "Incorrect Old Password"}, 422
        else:
            user = db.session().query(WeConnectUsers).filter_by(emailId=email_id).first()
            password = json["newPassword"]
            new_password = hashlib.md5(password.encode())
            new_password = new_password.hexdigest()
            user.password = new_password
            db.session().commit()

    @staticmethod
    def reset_password(self, email_id, json):
        user = db.session().query(WeConnectUsers).filter_by(emailId=email_id).first()
        password = json["newPassword"]
        new_password = hashlib.md5(password.encode())
        new_password = new_password.hexdigest()
        user.password = new_password
        db.session().commit()

    def post():
        try:
            if "email" in request.args and "otp" in request.args:
                json_data = request.get_json(force=True)
                if not json_data:
                    return {"message": "No input data provided"}, 400
                elif "newPassword" in json_data and "oldPassword" in json_data:
                    self.change_password(request.args["email"], json_data)
                elif "newPassword" in json_data:
                    if db.session().query(ForgotPasswordStatus).filter_by(emailId=request.args["email"], otp = request.args["otp"]).first():
                        db.session().query(ForgotPasswordStatus).filter_by(emailId=request.args["email"]).delete()
                        self.reset_password(request.args["email"], json_data)
                        db.session().commit()
                    else:
                        return {"message" : "Invalid OTP"}, 422
                else:
                    return {"message" : "Incorrect JSON Data"}, 422
            else:
                return {"message": "Incorrect format"}, 422
            return {"message": "Password Change Successful"}, 200
        except:
            return {"message" : "Something Went Wrong"}, 500