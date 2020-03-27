import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import request
from flask_restful import Resource

from model import db, ForgotPasswordStatus, WeConnectUsers


class ForgotPassword(Resource):
    def get(self):
        #try:
            email_id = request.args["email"]
            if db.session().query(WeConnectUsers).filter_by(emailId=email_id).first():
                if db.session().query(ForgotPasswordStatus).filter_by(emailId=email_id).first():
                    db.session().query(ForgotPasswordStatus).filter_by(emailId=email_id).delete()
                otp = ''.join(random.choice(string.digits) for _ in range(6))
                db.create_all()
                key = ForgotPasswordStatus(email_id, otp)
                server = smtplib.SMTP('smtp.gmail.com:587')
                server.ehlo()
                server.starttls()
                message = MIMEMultipart()
                message['From'] = "ayush1641138@gmail.com"
                message['To'] = email_id
                message['Subject'] = 'Forgot Password OTP - WeConnect'
                message.attach(MIMEText(
                    "Your OTP to create new password is: " + otp,
                    'plain'))
                text = message.as_string()
                server.login("ayush1641138@gmail.com", "Ayushanand@16")
                server.sendmail("ayush1641138@gmail.com", email_id, text)
                server.quit()
                db.session.add(key)
                db.session.commit()
                return {"message" : "Otp Sent"}, 200
            else:
                return {"message" : "Email id not registered"}, 409
        #except:
         #   return {"message" : "Something went wromg"}, 500
