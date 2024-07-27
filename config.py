import os
basedir = os.path.join(os.path.abspath(os.path.dirname(__file__)))

class Config(object):
    

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:////' + os.path.join(basedir, 'db','app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # high resolution image path
    IMG_DIR = os.environ.get('MIRTRON_SVG')
    
    SECRET_KEY = os.environ.get('SECRET_KEY') 
    WEB_NAME = 'mitronDB'

    # set mail to notify errors
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = 1

    MAIL_USERNAME = "mirtronbal@gmail.com"
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    ADMINS = [os.environ.get('ADMIN_MAIL')]





