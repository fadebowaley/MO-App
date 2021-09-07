import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_DEFAULT_SENDER = 'hello@brvcase.com'
    MAIL_SERVER = 'smtp-relay.sendinblue.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'fadebowaley@gmail.com'
    MAIL_PASSWORD = 'wt0yc4QX6VFsdnP9'
    ADMINS = ['hello@brvcase.com']    
    MAX_CONTENT_LENGTH = 1024 * 1024 * 1024 * 1024
    ALLOWED_EXTENSIONS = ['.jpg', '.png', '.gif', '.pdf', '.csv', 
    '.doc','docx', '.xls', '.xlsx','.txt']
    UPLOADED_ITEMS_DEST = 'upload'
    UPLOADED_PHOTOS_DEST = os.path.join(basedir, 'static')

    

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:ROOT@/mo-app'

    

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

