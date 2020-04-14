from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging, os
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "login"
mail = Mail(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

if not app.debug:
    if app.config["MAIL_SERVER"]:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mailHandler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='NanoBlog Failure',
            credentials=auth, secure=secure)
        mailHandler.setLevel(logging.ERROR)
        app.logger.addHandler(mailHandler)
    
    if not os.path.exists('logs'):
        os.mkdir('logs')
    fileHandler = RotatingFileHandler("logs/nanoblog.log", maxBytes=10240, backupCount=10)
    fileHandler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    fileHandler.setLevel(logging.INFO)
    app.logger.addHandler(fileHandler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('NanoBlog startup')

from app import routes, models, errors