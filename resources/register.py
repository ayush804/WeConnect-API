from flask_restful import Resource
from flask import request
from model import db, WeConnect_Users

class Register(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400

        emailId = json_data['emailId']
        password = json_data['password']
        sex = json_data['sex']
        dob = json_data['date']
        name = json_data['name']
        #query = "INSERT INTO WeConnect_Users (emailId, password, name, sex, dob) VALUES (" + emailId + "," + password + "," + name + "," + sex + "," + dob + ")"
        db.create_all()
        db.session.commit()
        #print(query)
        user = WeConnect_Users(emailId, password)
        db.session.add(user)
        db.session.commit()
        return {"message": "Registered"}