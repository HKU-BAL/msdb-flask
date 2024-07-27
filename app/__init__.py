from flask import Flask,request, current_app
from config import Config
from flask_babel import Babel, lazy_gettext as _l
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()
mail = Mail()
def prefix_route(route_function, prefix='', mask='{0}{1}'):
    '''
    Defines a new route function with a prefix.
    The mask argument is a `format string` formatted with, in that order:
      prefix, route
    '''
    def newroute(route, *args, **kwargs):
        '''New function to prefix the route'''
        return route_function(mask.format(prefix, route), *args, **kwargs)
    return newroute

def create_app(config_class=Config):

    app = Flask(__name__,static_folder='static', static_url_path='/msdb/static')
    
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
     
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)
    
    # register blueprints
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
 
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)



    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject=app.config['WEB_NAME']+' Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
        
        file_handler = RotatingFileHandler('logs/mirtronDB.log',
                                           maxBytes=100240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.ERROR)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.ERROR)
        app.logger.info(app.config['WEB_NAME']+' startup')

    return app


