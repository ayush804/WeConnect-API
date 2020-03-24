from flask_restful import Resource
from flask import request
from model import db, WeConnect_Users


class Register(Resource):
    def post(self):
        try:
            json_data = request.get_json(force=True)
            sex, name="", ""
            dob = None
            if not json_data:
                return {"message": "No input data provided"}, 400
            if "emailId" in json_data:
                emailId = json_data['emailId']
            else:
                return {"message" : "Missing Email id"}, 422
            if db.session().query(WeConnect_Users).filter_by(emailId=emailId).first():
                return {"message" : "User already exist"}, 409
            if "password" in json_data:
                password = json_data['password']
            else:
                return {"response": "Missing Password"}
            if "sex" in json_data:
                sex = json_data['sex']
            if "dob" in json_data:
                dob = json_data['dob']
            if "name" in json_data:
                name = json_data['name']
            db.create_all()
            db.session.commit()
            user = WeConnect_Users(emailId, password, sex, dob, name)
            db.session.add(user)
            db.session.commit()
            return {"message": "User Created"}, 201
        except:
            return {"message" : "Something went wrong"}, 500