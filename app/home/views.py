import re
from app.home import bp
from flask import abort, render_template,flash, redirect, url_for, request
from flask_login import current_user, login_required
from sqlalchemy import func, and_
from datetime import datetime, date, timedelta
from app import db, session, sessionmaker
from app.auth.email import  send_set_email
from app.models import  User


 #add admin dashboard view
@bp.route('/dashboard')
@login_required
def admin_dashboard():
    pass    
    

@bp.route('/')
def homepage():
    return render_template('home/home.html')


@bp.route('/pricing')
def pricing():
    return render_template('home/pricing.html')

def username_from(email):
    result = re.search(r'([\w\d\.]+)@[\w\d\.]+', email)
    if result and email.count('@') == 1:
        return result.group(1)
    else:
        ValueError(f'{email} is not a validly formatted e-mail address.')



@bp.route('/features')
def features():
    return render_template('home/features.html')


@bp.route('/contact')
def market():
    return render_template('home/contact.html')



@bp.route('/about')
def error():
    return render_template('home/about.html')


@bp.route('/privacy')
def policy():
    return render_template('home/privacy-policy.html')