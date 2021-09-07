import os
import secrets
import string
import json
import shutil
import random
import dateutil.relativedelta
import dateutil.parser
import dateutil.rrule
import calendar
import pathlib
import pdfkit
from pathlib import Path
import emoji
from datetime import datetime, date
from flask import abort, flash, redirect, render_template, \
url_for, g, jsonify, current_app, request, make_response
from flask_login import current_user, login_required
from wtforms import ValidationError
from werkzeug.utils import secure_filename
from hashlib import md5
from PIL import Image
from ..decorators import admin_required, permission_required, account_required,\
    manager_required, super_required
from app.admin import bp
from app import db, session, sessionmaker
from app.models import  User

# @bp.app_context_processor
# def inject_permissions():
#     return dict(Permission=Permission)


"""
1. views for the shop
2. forms for listings
3. 
"""

