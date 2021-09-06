#third party import
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from faker import Faker
from flask import Flask, request, current_app
from flask_moment import Moment
from flask_pagedown import PageDown
from flask_debugtoolbar import DebugToolbarExtension
from config import config
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_assets import Bundle, Environment
from sqlalchemy.orm import sessionmaker

 # global scope  
Session = sessionmaker(autoflush=False)  

fake = Faker()
session = Session()
db = SQLAlchemy()
pagedown = PageDown()
migrate = Migrate()
login = LoginManager()
# login_manager.session_protection = 'strong'
login.login_view = 'auth.login'
#login.login_message = _l('Please log in to access this page.')
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()

def create_app(config_name):
    app = Flask(__name__)
    app.debug = True
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)    
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    pagedown.init_app(app)

    
    # checking to enable debug mode
    if app.debug:
        from werkzeug.debug import DebuggedApplication
        app.wsgi_app = DebuggedApplication(app.wsgi_app, True)
        

    
    
    #Blue print for Admin , Auth and Home
    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    from app.account import bp as account_bp
    app.register_blueprint(account_bp, url_prefix='/account')

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.settings import bp as settings_bp
    app.register_blueprint(settings_bp, url_prefix='/settings')
    
    from app.payments import bp as payments_bp
    app.register_blueprint(payments_bp, url_prefix='/payments')
    
    from app.home import bp as home_bp
    app.register_blueprint(home_bp)
    
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    #loading the js file 
    js = Bundle('app.js', 'bootstrap-datetimepicker.min.js', 'bootstrap.min.js', 'chart.js', 'dataTables.bootstrap4.min.js', 'dropfiles.js','fullcalendar.min.js', 'jquery.ui.touch-punch.min.js', 'jquery.slimscroll.min.js', 'mask.js', 'moment.min.js', 'multiselect.min.js', 'popper.min.js', 'select2.min.js','main.js', 'task.js', 'jquery-3.2.1.min.js','jquery.ui.touch-punch.min.js','jquery.maskedinput.min.js','chart.js','jquery.dataTables.min.js',   output='gen/fade.js' )
    # style_bundle=Bundle('bootstrap.min.css', 'font-awesome.min.css','line-awesome.min.css','style.css', 'select2.min.css','fullcalendar.min.css', 'font-awesome.min.css','dataTables.bootstrap4.min.css', 'bootstrap-datetimepicker.min.css',  output='gen/fade.css'  )
    style_bundle=Bundle('css/bootstrap2.min.css', 'css/font-awesome2.min.css','css/line-awesome2.min.css','css/style2.css', 'css/select2.2.min.css','css/fullcalendar2.min.css', 'css/font-awesome2.min.css','css/dataTables2.bootstrap4.min.css', 'css/bootstrap2-datetimepicker.min.css',  output='gen/fade.css'  )
    # css and js files for hompages and frontend
    homecss = Bundle('css/app.css', 'css/core.css', output = 'gen/home.css')
    homejs = Bundle('app_home.js', 'core_home.js', output = 'gen/home.js' )
    assets = Environment(app)
    assets.register('main_js', js)
    assets.register('main_styles', style_bundle)
    assets.register('home_js', homejs)
    assets.register('home_styles', homecss)
    

    return app



