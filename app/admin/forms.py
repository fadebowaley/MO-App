from flask_wtf import  FlaskForm
from wtforms import Form, FieldList, StringField, StringField, SubmitField, BooleanField, \
 PasswordField,  TextAreaField, SubmitField, FormField, SelectField,\
  FileField, IntegerField, TextField, FieldList
from wtforms.validators import DataRequired, Length,ValidationError, InputRequired
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.html5 import DateTimeField, DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import ValidationError, DataRequired, Length
#from flask_babel import _, lazy_gettext as _l
from flask_login import current_user, login_required
from app.models import  User



