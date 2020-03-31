from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

import logging
from logging.handlers import SMTPHandler

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'login'
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.chats import bp as chat_bp
    app.register_blueprint(chat_bp)

    from app.connections import bp as connections_bp
    app.register_blueprint(connections_bp)

    # from app.emails import bp as emails_bp
    # app.register_blueprint(emails_bp)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)


    # if not app.debug and not app.testing:
    #     init_mail_debug(app)

    return app


def init_mail_debug(app):
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='PlaceHolder Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


from app import models