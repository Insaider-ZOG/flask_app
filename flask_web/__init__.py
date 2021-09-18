from flask import Flask
from flask_migrate import Migrate
from flask_web.config import DevelopmentConfig


migrate = Migrate()


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(DevelopmentConfig)

    from .models import dbase
    dbase.init_app(app)

    from .shemas import mallow
    mallow.init_app(app)
    migrate.init_app(app, dbase)

    from .views import jwt, login_manager
    jwt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"

    from .views import account_bp, post_bp, category_bp, comment_bp
    app.register_blueprint(account_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(comment_bp)

    return app