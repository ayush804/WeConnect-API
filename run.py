from flask import Flask, Blueprint


def create_app(config_filename):
    application = Flask(__name__)
    application.config.from_object(config_filename)

    from app import api_bp
    application.register_blueprint(api_bp, url_prefix='/api')

    from model import db
    db.init_app(application)

    return application


if __name__ == "__main__":
    app = create_app("config")
    app.run(debug=True)