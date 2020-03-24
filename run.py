from flask import Flask, Blueprint


def create_app(config_filename):
    application = Flask(__name__)
    application.config.from_object(config_filename)

    application.register_blueprint(Blueprint('api', __name__), url_prefix='/api')

    from model import db
    db.init_app(application)

    return application


if __name__ == "__main__":
    application = create_app("config")
    application.run()