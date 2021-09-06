from datetime import datetime, date
import dateutil.relativedelta
import dateutil.parser
import dateutil.rrule
import calendar
from flask import abort, flash, redirect, render_template, \
url_for, g, jsonify, current_app, request
from flask_login import current_user, login_required
from wtforms import ValidationError
import os
import secrets
import string
import random
from werkzeug.utils import secure_filename
import pathlib
from pathlib import Path
import emoji
from hashlib import md5
from PIL import Image
from app.admin import bp
from app import db, session, sessionmaker
from app.models import User


ALLOWED_EXTENSIONS = set(['.jpg', '.png', '.gif', '.pdf', '.csv', '.doc','docx', '.xls', '.xlsx','.txt' ])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def  set_status(a):
    a == True

       

@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    #g.locale = str(get_locale())



# """ this section is for my account page """