from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


ma = Marshmallow()
db = SQLAlchemy()


class WeConnect_Users(db.Model):
    __tablename__ = 'WeConnect_Users'
    emailId = db.Column(db.String(250), primary_key=True)
    password = db.Column(db.String(250), nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    name = db.Column(db.String(250))
    sex = db.Column(db.String(250))
    dob = db.Column(db.Date)

    def __init__(self, emailId, password, sex, dob, name):
        self.emailId = emailId
        self.password = password
        self.sex = sex
        self.dob = dob
        self.name = name