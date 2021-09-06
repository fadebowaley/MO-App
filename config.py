import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

#class Config(object):
    #SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        #'sqlite:///' + os.path.join(basedir, 'expartio.db')

class Config:
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    # This is for windows
    # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:root@/nuparty'
    

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_DEFAULT_SENDER = 'hello@brvcase.com'
    MAIL_SERVER = 'smtp-relay.sendinblue.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'fadebowaley@gmail.com'
    MAIL_PASSWORD = 'wt0yc4QX6VFsdnP9'
    ADMINS = ['hello@brvcase.com']    
    # MAIL_SERVER = os.environ.get('MAIL_SERVER')
    # MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # ADMINS = ['hello@brvcase.com']
    MAX_CONTENT_LENGTH = 1024 * 1024 * 1024 * 1024
    ALLOWED_EXTENSIONS = ['.jpg', '.png', '.gif', '.pdf', '.csv', '.doc','docx', '.xls', '.xlsx','.txt' ]
    UPLOADED_ITEMS_DEST = 'upload'
    UPLOADED_PHOTOS_DEST = os.path.join(basedir, 'static')
    # SERVER_NAME = 'localhost:5000'
    

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
    # 'sqlite:///' + os.path.join(basedir, 'foldate.db')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:ROOT@/briefcase'
    #x=y

    

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)



config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

