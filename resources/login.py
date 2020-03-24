from flask_jwt_extended import create_access_token
from flask_restful import Resource
from flask import request
from model import db, WeConnect_Users


class Login(Resource):
    def post(self):
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
            if db.session().query(WeConnect_Users).filter_by(emailId=emailId, password=password).first():
                token = create_access_token(identity=emailId)
                return {"message" : "Authenticated successfully", "token": token}, 200
            else:
                return {"message" : "Invalid Username or Password"}, 401
        except:
            return {"message" : "Something went wrong"}, 500