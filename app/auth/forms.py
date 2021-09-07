from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, \
    ValidationError, BooleanField, SelectField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.html5 import DateTimeField, DateField
from flask_login import current_user
from app.models import User, Role
from .email import send_email



def select_roles():        
    if not current_user.role.permissions == 31:        
        roles = Role.query.all()           
     
    return roles



class RegistrationForm(FlaskForm):
    """  Form for Users to create new account   """
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirm Password')    
    role = QuerySelectField('Select a User', validators=[DataRequired()], query_factory=select_roles, get_label='name',
                            allow_blank=True, blank_text=(u'--- Select your roles ---')) 
    submit = SubmitField('Register')
 
        
        
        
        

class LoginForm(FlaskForm):
    """  Form for users to login    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')



class ResetPasswordRequestForm(FlaskForm):
    email = StringField('', validators=[DataRequired(), Email()])
    submit = SubmitField('Click to here to send password')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email address. Register first')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset password')
    
    
class VendorForm(FlaskForm):
    """  Form for creating Company """
    company = StringField('Company Name',validators=[DataRequired()])
    company_address =  TextAreaField(' Company Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    country= SelectField(u'Country', choices=[('Nigeria', 'Nigeria'), ('United Kingdom', 'United Kingdom'), ('United States', 'United States'), ('Ghana', 'Ghana'), ('United Arab Emirates', 'United Arab Emirates'), 
    ('South Africa', 'South Africa'), ]) 
    postal_code = StringField('Postal Code', validators=[DataRequired()])
    company_email = StringField('Company Email Address', validators=[DataRequired()])
    phone_number= StringField('Company Contact Number', validators=[DataRequired()])
    logo_file = FileField('Update Company Logo', validators=[FileAllowed(['jpg', 'png'])])
    contact_person = StringField('Contact Person', validators=[DataRequired()])
    contact_phone = StringField('Contact Phone', validators=[DataRequired()])
    website = StringField('Website:', validators=[DataRequired()])
    
    role = QuerySelectField('Select a User', validators=[DataRequired()], query_factory=select_roles, get_label='name',
                            allow_blank=True, blank_text=(u'--- Select your roles ---')) 
    submit = SubmitField('Submit')



