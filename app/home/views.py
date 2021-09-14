import re
from app.home import bp
from flask import abort, render_template,flash, redirect, url_for, request
from flask_login import current_user, login_required
from sqlalchemy import func, and_
from datetime import datetime, date, timedelta
from app import db, session, sessionmaker
from app.auth.email import  send_set_email
from app.models import  User



@bp.route('/')
def homepage():
    return render_template('home/home.html')



def username_from(email):
    result = re.search(r'([\w\d\.]+)@[\w\d\.]+', email)
    if result and email.count('@') == 1:
        return result.group(1)
    else:
        ValueError(f'{email} is not a validly formatted e-mail address.')




