from flask import Flask, Blueprint

application = Flask(__name__)
#def create_app(config_filename):
application.config.from_object("config")
from app import api_bp
application.register_blueprint(api_bp, url_prefix='/api')

from model import db
db.init_app(application)

    #return application


if __name__ == "__main__":
    #application = create_app("config")
    application.run(debug=True)