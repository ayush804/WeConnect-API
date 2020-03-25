from flask_jwt_extended import create_access_token
from flask_restful import Resource
from flask import request
from model import db, WeConnect_Users
import re


class Login(Resource):
    def post(self):
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        try:
            json_data = request.get_json(force=True)
            if not json_data:
                return {"message": "No input data provided"}, 400
            if "emailId" in json_data:
                emailId = json_data["emailId"]
            else:
                return {"message": "Missing Email id"}, 422
            if "password" in json_data:
                password = json_data['password']
            else:
                return {"message": "Missing Password"}
            if re.search(regex, emailId):
                if db.session().query(WeConnect_Users).filter_by(emailId=emailId).first():
                    user = db.session().query(WeConnect_Users).filter_by(emailId=emailId).first()
                    if user.__dict__["password"] == password:
                        token = create_access_token(identity=emailId)
                        return {"message" : "Authenticated successfully", "Token": token,
                                "Name": user.__dict__["name"], "DateofBirth" : user.__dict__["dob"],
                                "Sex" : user.__dict__["sex"]}, 200
                    else:
                        return {"message" : "Incorrect Password"}
                else:
                    return {"message" : "Email id not registered"}, 401
            else:
                return {"message" : "Email id is not in valid format"}, 422
        except:
            return {"message" : "Something went wrong"}, 500