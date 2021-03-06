from flask import request
from flask_restful import Resource

from model import db, VerificationStatus, WeConnectUsers


class VerifyEmail(Resource):
    def get(self):
        try:
            if db.session().query(VerificationStatus).filter_by(emailId=request.args["email"], verificationKey=request.args["key"]).first():
                email_status = db.session().query(WeConnectUsers).filter_by(emailId=request.args["email"]).first()
                email_status.isVerified = True
                db.session().query(VerificationStatus).filter_by(emailId=request.args["email"]).delete()
                db.session.commit()
                return {"message" : "Verified Successfully."}, 200
            else:
                return {"message" : "Incorrect Key"}, 422
        except:
            return {"message" : "Something went wrong"}, 500