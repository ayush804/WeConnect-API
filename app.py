from flask import Blueprint
from flask_restful import Api

from resources.changePassword import ChangePassword
from resources.forgotPassword import ForgotPassword
from resources.login import Login
from resources.register import Register
from resources.verifyemail import VerifyEmail

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(VerifyEmail, '/verifyEmail')
api.add_resource(ForgotPassword, '/forgotPassword')
api.add_resource(ChangePassword, '/changePassword')