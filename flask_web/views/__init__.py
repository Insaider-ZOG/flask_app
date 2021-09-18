from flask.blueprints import Blueprint
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_login import LoginManager

jwt = JWTManager()
login_manager = LoginManager()

account_bp = Blueprint("account", __name__)
account_api = Api(account_bp)
post_bp = Blueprint('post', __name__)
post_api = Api(post_bp)
category_bp = Blueprint('category', __name__)
category_api = Api(category_bp)
comment_bp = Blueprint('comment', __name__)
comment_api = Api(comment_bp)

from . import account_views, post_views, category_views, comment_views