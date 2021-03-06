from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


ma = Marshmallow()
db = SQLAlchemy()


class WeConnectUsers(db.Model):
    __tablename__ = 'WeConnectUsers'
    emailId = db.Column(db.String(250), primary_key=True)
    password = db.Column(db.String(250), nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    name = db.Column(db.String(250))
    sex = db.Column(db.String(250))
    dob = db.Column(db.Date)
    isVerified = db.Column(db.Boolean, default = False)

    def __init__(self, email_id, password, sex, dob, name):
        self.emailId = email_id
        self.password = password
        self.sex = sex
        self.dob = dob
        self.name = name


class VerificationStatus(db.Model):
    __tablename__ = 'VerificationStatus'
    emailId = db.Column(db.String(250), primary_key=True)
    verificationKey = db.Column(db.String(250))

    def __init__(self, email_id, verification_key):
        self.emailId = email_id
        self.verificationKey = verification_key


class ForgotPasswordStatus(db.Model):
    __tablename__ = 'ForgotPasswordStatus'
    emailId = db.Column(db.String(250), primary_key=True)
    otp = db.Column(db.String(250))

    def __init__(self, email_id, otp):
        self.emailId = email_id
        self.otp = otp


class WeConnectPosts(db.Model):
    __tablename__ = 'WeConnectPosts'
    postId = db.Column(db.Integer, primary_key=True)
    emailId = db.Column(db.String(250))
    text = db.Column(db.String(999999))
    images = db.Column(db.String(999999), primary_key=True)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, email_id, text, images):
        self.emailId = email_id
        self.images = images
        self.text = text
