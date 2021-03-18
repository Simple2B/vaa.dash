import os

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from werkzeug.exceptions import HTTPException

from app.logger import log


# instantiate extensions
login_manager = LoginManager()
db = SQLAlchemy()
mail = Mail()
bootstrap = Bootstrap()
log.set_level(log.DEBUG)


def create_app(environment="development"):

    from config import config
    from app.models import (
        User,
        AnonymousUser,
    )
    from app.views import (
        main_blueprint,
        auth_blueprint,
    )
    from app.dashapps import bp as bp_dashapps

    from app.dashapps.dash_analysis.app import add_dash as ad1
    from app.dashapps.dash_yield_curve.app import add_dash as ad2
    from app.dashapps.dash_oil_and_gas.app import add_dash as ad3

    # Instantiate app.
    app = Flask(__name__)

    # Set app config.
    env = os.environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])
    config[env].configure(app)

    # Set up email.
    mail.init_app(app)

    # Set up extensions.
    db.init_app(app)
    login_manager.init_app(app)

    # Set up bootstrap extension
    bootstrap.init_app(app)

    # Register blueprints.
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(bp_dashapps)

    app = ad1(app)
    app = ad2(app)
    app = ad3(app)

    # Set up flask login.
    @login_manager.user_loader
    def get_user(id):
        return User.query.get(int(id))

    login_manager.login_view = "auth.signin"
    login_manager.login_message_category = "info"
    login_manager.anonymous_user = AnonymousUser

    # Error handlers.
    @app.errorhandler(HTTPException)
    def handle_http_error(exc):
        return render_template("error.html", error=exc), exc.code

    return app
