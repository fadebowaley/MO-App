from flask_wtf import  FlaskForm
from wtforms import Form, FieldList, StringField, StringField, SubmitField, BooleanField, \
 PasswordField,  TextAreaField, SubmitField, FormField, SelectField,\
  FileField, IntegerField, TextField, FieldList
from wtforms.validators import DataRequired, Length,ValidationError, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.html5 import DateTimeField, DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import ValidationError, DataRequired, Length
from app.models import Chamber, User, Role



class ChamberModuleForm(FlaskForm):
    """form for Updating the Module Settings """
    is_immigration = BooleanField(validators=[DataRequired(), ])
    is_probate = BooleanField(validators=[DataRequired(), ])
    is_ent = BooleanField(validators=[DataRequired(), ])
    is_realestate = BooleanField(validators=[DataRequired(), ])
    is_services = BooleanField(validators=[DataRequired(), ])
    is_Iproperty = BooleanField(validators=[DataRequired(), ])
    is_Billings = BooleanField(validators=[DataRequired(), ])


class ChamberForm(FlaskForm):
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
    submit = SubmitField('Submit')
    
    
    
class RegistrationForm(FlaskForm):
    """  Form for Users to create new account   """
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirm Password')
    chamber = QuerySelectField('Company Posted', query_factory=lambda: Chamber.query.all(), get_label="company")
    role = QuerySelectField('Select Role', query_factory=lambda:Role.query.all(), get_label="name")
    
    submit = SubmitField('Register')
 
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
          
          

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm new password',
                              validators=[DataRequired()])
    submit = SubmitField('Update Password')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    submit = SubmitField('Reset Password')


class PasswordResetForm(FlaskForm):
    password = PasswordField('New Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')


class ChangeEmailForm(FlaskForm):
    email = StringField('New Email', validators=[DataRequired(), Length(1, 64),
                                                 Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Update Email Address')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered.')




class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    first_name = StringField('First name' )
    last_name = StringField('Last name')
    phone_number=StringField('Phone Number')
    company = StringField('Company/organisation' )
    gender = SelectField(u'Gender', choices=[('Male', 'Male'), ('Female', 'Female')])
    company_address = StringField('Company Address' ) 
    city = StringField('City')
    state = SelectField(u'State', choices=[('Lagos', 'Lagos'), ('Abia','Abia'), ('Abia','Abia'), 
    ('Adamawa', 'Adamawa'),('Akwa Ibom', 'Akwa Ibom'),
    ('Anambra', 'Anambra'),('Bauchi', 'Bauchi'),('Bayelsa', 'Bayelsa'),
    ('Benue', 'Benue'),('Borno', 'Borno'),('Cross River', 'Cross River'),
    ('Delta', 'Delta'),('Ebonyi', 'Ebonyi'),('Edo', 'Edo'),('Ekiti', 'Ekiti'),
    ('Enugu', 'Enugu'),('FCT - Abuja', 'FCT - Abuja'),('Gombe', 'Gombe'),
    ('Imo', 'Imo'),('Jigawa', 'Jigawa'),('Kaduna','Kaduna'),('Kano', 'Kano'),
    ('Katsina', 'Katsina'),('Kebbi', 'Kebbi'),('Kogi', 'Kogi'),
    ('Kwara', 'Kwara'),('Lagos', 'Lagos'),('Nasarawa', 'Nasarawa'),
    ('Niger', 'Niger'),('Ogun', 'Ogun'),('Ondo', 'Ondo'),('Osun', 'Osun'),
    ('Oyo', 'Oyo'),('Plateau', 'Plateau'),('Rivers', 'Rivers'),('Sokoto', 'Sokoto'),
    ('Taraba', 'Taraba'),('Yobe', 'Yobe'),('Zamfara', 'Zamfara') ]),
    date_created= DateField('Effective Date ', format='%Y-%m-%d')
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')          

    

# class configurationForm (Flaskform):
#      """ form to set all kind of configuration for the portal. the following will be asked
#      Self-Service Portal
#      Immigration Sservices
#      Real Estates
#      Probate Services
#      Entertainment
#      Vendor Services
#      relationship with Chamber
#      """







""" here we implement the forms for property
all business logic etc"""

"""
The following steps need to quickly be developed
1. A Form that captured property details (CRUD) + Upload
2. Model relationship between Client and Property
* We can select a client and add property by ID
3. Fuction that determines Recurring Transaction(Annually)
4. Boolean for Transaction -  Sales or Lease/Rent
5. Boolean for Ownership -  Commercial or Private
6. Boolean for Status - Serched(CofO), Others


##Table 1 -  Display tables for property by lease or sales
1. Special table for property with their date of renewal
2. Property sold or not sold

## Table 2 - TASK - PREDEFINED DOCUMENT
1. Prepare document for agreement (Property)
2. prepare document for sales (property)
3. prepare document for reminder of rents 

## TASK 3  -  REPORT GENERATION
1. Generate real estate report by ssles
2. Generate real estate report by leases/rent
3. Generate Real Estate report by Search
"""

