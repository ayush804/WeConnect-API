from flask import Flask, Blueprint
from app import api_bp
from model import db
from flask_jwt_extended import JWTManager


application = Flask(__name__)
application.config.from_object("config")
application.register_blueprint(api_bp, url_prefix='/api')
db.init_app(application)
application.config['SECRET_KEY'] = 'super-secret'
jwt = JWTManager(application)


def create_app(config_filename):
    global application
    return application


if __name__ == "__main__":
    application.run(debug=True)