from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

from stock_data.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
mail = Mail()


def create_app(config_class=Config):
    flask_app = Flask(__name__)
    flask_app.config.from_object(config_class)

    db.init_app(flask_app)
    bcrypt.init_app(flask_app)
    login_manager.init_app(flask_app)
    mail.init_app(flask_app)

    from stock_data.stock_app.routes import stock
    from stock_data.crypto_currency.routes import crypto
    from stock_data.users.routes import users
    from stock_data.errors.handlers import errors
    flask_app.register_blueprint(stock)
    flask_app.register_blueprint(crypto)
    flask_app.register_blueprint(users)
    flask_app.register_blueprint(errors)

    return flask_app
