import hashlib
from flask_jwt_extended import create_access_token
from flask_restful import Resource
from flask import request
from model import db, WeConnectUsers
import re


class Login(Resource):
    @staticmethod
    def post():
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        try:
            json_data = request.get_json(force=True)
            if not json_data:
                return {"message": "No input data provided"}, 400
            if "emailId" in json_data:
                email_id = json_data["emailId"]
            else:
                return {"message": "Missing Email id"}, 422
            if "password" in json_data:
                password = json_data['password']
                password = hashlib.md5(password.encode())
                password = password.hexdigest()
            else:
                return {"message": "Missing Password"}, 422
            if re.search(regex, email_id):
                if db.session().query(WeConnectUsers).filter_by(emailId=email_id).first():
                    user = db.session().query(WeConnectUsers).filter_by(emailId=email_id).first()
                    if user.__dict__["password"] == password:
                        token = create_access_token(identity=email_id)
                        return {"message": token, "isVerified" : user.__dict__["isVerified"]}, 200
                    else:
                        return {"message" : "Incorrect Password"}, 422
                else:
                    return {"message" : "Email id not registered"}, 401
            else:
                return {"message" : "Email id is not in valid format"}, 422
        except:
            return {"message" : "Something went wrong"}, 500