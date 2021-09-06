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
from app.models import  Employee, Quota, Cerpac ,Emergency,\
     Company, Lap, Token_serial, Renew, Folder, File



class EmployeeForm(FlaskForm):
    """    Form for admin to add or edit or Update Employee Details    """
    email = StringField('Email Address')  
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    phone_number = StringField('Phone Number' )
    gender = SelectField(u'Gender', choices=[('Male', 'Male'), ('Female', 'Female')])
    address = StringField('Residential Address' ) 
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
    ('Taraba', 'Taraba'),('Yobe', 'Yobe'),('Zamfara', 'Zamfara') ])
    country = SelectField(u'Country', choices=[('Nigeria', 'Nigeria'), ('Ghana', 'Ghana'), ('Ghana', 'Ghana'), ('Rwanda', 'Rwanda'), ('Ivory coast', 'Ivory coast'), 
    ('South Africa', 'South Africa'), ])    
    birthday = DateField('Employee Birthday', format='%Y-%m-%d')
    date_of_employment = DateField('Employment Date', format='%Y-%m-%d')
    passport_pic = FileField('Employee Picture')
    employee_id = StringField(' Employee ID')
    expat_id = StringField(' Employee ID')
    create_folder = BooleanField('A new folder will be created for this client, kindly uncheck ', default='False' )
    is_immigration = BooleanField('Check for Immigration Account', default='False' )
    is_probate = BooleanField('Check for probate account ', default='False' )
    is_realestate = BooleanField('Check for Real Estate account', default='False' )
    is_ent = BooleanField('Check for Entertainment account ', default='False' )
    #role = QuerySelectField('Select Role', query_factory=lambda: Role.query.all(), get_label="name")
    laps = QuerySelectField('Quota Position', query_factory=lambda: Lap.query.all(), get_label="runner_name")
    company = QuerySelectField('Company Posted', query_factory=lambda: Company.query.all(), get_label="company_name")
    submit = SubmitField('Submit')


class EmergencyForm(FlaskForm):
    """    Form for admin to add or edit or Update Employee Family Details    """
    name = StringField('Contact Name')
    phone = StringField('Contact Phone Number')
    address = TextAreaField('Contact Address')
    relationship = SelectField(u'Relationship', choices=[('Spouse', 'Spouse'), ('Brother', 'Brother'), ('Sister', 'Sister'), ('Uncle', 'Uncle'), ('Aunt', 'Aunt')])    
    employee= QuerySelectField('Emergency Contact', query_factory=lambda: Employee.query.all(), get_label="last_name")
    submit = SubmitField('Submit')


class CerpacForm(FlaskForm):
    """    Form for admin to add or edit or Update Cerpac Details    """
    cerpac_issue_date = DateField('Cerpac Issue Date', format='%Y-%m-%d')
    expired_date = DateField('Cerpac Expiry Date', format='%Y-%m-%d')
    cerpac_serial_no = StringField('Cerpac Reference Number', validators=[DataRequired()])
    cerpac_upload = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])]),
    ccn_number = StringField('Cerpac Number', validators=[DataRequired()])
    submit = SubmitField('Submit')


class RoleForm(FlaskForm):
    """  Form for admin to add or edit a role  """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

    

class CompanyForm(FlaskForm):
    """  Form for admin to add or edit a company """
    company_name=StringField('Company Name',validators=[DataRequired()])
    company_address =  TextAreaField(' Company Address', validators=[DataRequired()])
    company_email = StringField('Company Email Address', validators=[DataRequired()])
    
    contact_number= StringField('Contact Person Number', validators=[DataRequired()])
    company_number= StringField('Company Contact Number', validators=[DataRequired()])
    contact_person= StringField('Contact Person', validators=[DataRequired()])
    nature = SelectField(u'Industry', choices=[('Manufacturing', 'Manufacturing'), ('Legal Services', 'Legal Services'), ('Information Technology', 'Information Technology'), ('Service Providers', 'Service Providers'), ('Others', 'Others'), 
    ('South Africa', 'South Africa'), ])  
    
    logo_image = FileField('Update Company Logo', validators=[FileAllowed(['jpg', 'png'])])
    city = StringField('City')
    postal_code = StringField('Postal Code', validators=[DataRequired()])
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
    ('Taraba', 'Taraba'),('Yobe', 'Yobe'),('Zamfara', 'Zamfara') ])
    country = SelectField(u'Country', choices=[('Nigeria', 'Nigeria'), ('Ghana', 'Ghana'), ('Ghana', 'Ghana'), ('Rwanda', 'Rwanda'), ('Ivory coast', 'Ivory coast'), 
    ('South Africa', 'South Africa'), ])  
    
    submit = SubmitField('Submit')

    
    
class PassportForm(FlaskForm):
    """  Form for admin to add or edit a passport details """
    employee = QuerySelectField(query_factory=lambda: Employee.query.all(), get_label="last_name")
    nationality =StringField(' Nationality', validators=[DataRequired()])
    passport_no = StringField('Passport Number', validators=[DataRequired()])
    passport_exp_date = DateField('Expiry Date ', format='%Y-%m-%d')
    passport_issue_date   = DateField('Issue Date ', format='%Y-%m-%d')     
    submit = SubmitField('Submit')
    

        
class DependentForm(FlaskForm):
    """  Form for admin to add or edit a passport details """
    employee = QuerySelectField(query_factory=lambda: Employee.query.all(), get_label="last_name")
    name =StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    relationship = SelectField(u'Relationship', choices=[('Spouse', 'Spouse'), ('Son', 'Son'), ('Daughter', 'Daughter'), ('Father', 'Father'), ('Mother', 'Mother')]) 
    birthday = DateField('Birthday', format='%Y-%m-%d')
    gender = SelectField(u'Gender', choices=[('Male', 'Male'), ('Female', 'Female')]) 
    submit = SubmitField('Submit')
    
    
    
class QuotaForm(FlaskForm):
    """  Form for admin to add or edit a Quota Details. 
    The Company is Selected from the database first, then Quota is added
    """
    quota_renewal_date = DateField('Renewal Date ', format='%Y-%m-%d')
    quota_exp_date =  DateField('Expiry Date ', format='%Y-%m-%d')
    effective_date= DateField('Effective Date ', format='%Y-%m-%d')
    quota_reference = StringField('Quota Reference')
    no_of_positions = SelectField(u'No of Quota positions', choices=[('1', '1'), ('2', '2'),  ('3', '3'),  ('4', '4'),  ('5', '5'),  ('6', '6'),  ('7', '7'), ('8', '8'),  ('9', '9'),  ('10', '10'),  ('11', '11'),  ('12', '12'),  ('13', '13'),  ('14', '14'),  ('15', '15'), ('16', '16'),  ('17', '17'),  ('18', '18'),  ('19', '19'),  ('20', '20')])
    quota_upload = FileField('Update Quota Document', validators=[FileAllowed(['jpg', 'png'])])
    company = QuerySelectField(query_factory=lambda: Company.query.all(), get_label="company_name")
    token_serial = QuerySelectField(query_factory=lambda: Token_serial.query.all(), get_label="serial_no")
    submit = SubmitField('Submit')

class QuotaPositionForm(FlaskForm):
      position =  StringField('Quota Position', validators=[DataRequired()])
      quota = QuerySelectField(query_factory=lambda: Quota.query.all(), get_label="quota_reference")
      submit = SubmitField('Submit')


class RenewForm(FlaskForm):
    """  Form for admin to renew passport details """
    cerpac_exp_date = DateField('Expiry Date ', format='%Y-%m-%d')
    cerpac_designation = StringField('Cerpac Designation')
    cerpac_reference = StringField('Cerpac Reference')
    quota_issue_date = DateField('Expiry Date ', format='%Y-%m-%d')
    quota_exp_date = DateField('Expiry Date ', format='%Y-%m-%d')
    quota_reference = StringField('Quota Designation')
    passport_issue_date = DateField('Expiry Date ', format='%Y-%m-%d')
    passport_exp_date = DateField('Expiry Date ', format='%Y-%m-%d')
    visa_issue_date = DateField('Expiry Date ', format='%Y-%m-%d')
    visa_expiry_date = DateField('Expiry Date ', format='%Y-%m-%d')
    visa_reference = StringField('Quota Designation')
    submit = SubmitField('Submit')
    
    



class CerpacRenewForm(FlaskForm):
    reference = QuerySelectField(query_factory=lambda: Cerpac.query.all(), get_label="cerpac_serial_no")
    issueDate = DateField('Expiry Date ', format='%Y-%m-%d')
    expiryDate = DateField('Expiry Date ', format='%Y-%m-%d')
    reference = StringField('Cerpac Reference')
    submit = SubmitField('Submit')






def getEmployee():
    
    if not current_user.role.permissions == 31:
                  
        employee = Employee.query.filter(Employee.accountid == current_user.chamber_id 
        ).filter(Employee.lap_id.is_(None))
    
    else:
                
        employee=Employee.query.filter(Employee.lap_id.is_(None))
      
    return employee
  
    

class AssignForm(FlaskForm):
    
    # employee = QuerySelectField( query_factory=lambda: Employee.query.filter(Employee.accountid == current_user.chamber_id).all(), 
    #                             get_label="label", allow_blank=True, blank_text=(u'---SELECT AN EXPATRIATE---'))
    
    employee = QuerySelectField('Select a User', validators=[DataRequired()], query_factory=getEmployee, get_label='label',
                            allow_blank=True, blank_text=(u'---SELECT AN EXPATRIATE---'))
    
   
    position = QuerySelectField(query_factory=lambda: Lap.query.all(), 
                                get_label="runner_name", allow_blank=True, blank_text=(u'Select Position'))
    submit = SubmitField('Submit')



""" This is a test form for dynamic addition for a child table"""


class LapForm(Form):
    """Subform.
    CSRF is disabled for this subform (using `Form` as parent class) because
    it is never used by itself.
    """
    runner_name = StringField('Quota position')
    

class Token_serialForm(Form):
    """
    CSRF is disabled for this subform (using `Form` as parent class) because
    it is never used by itself.
    """
    serial_no = StringField('Serial No')    
   


class MainForm(FlaskForm):
    """Parent form."""
    laps = FieldList( FormField(LapForm),  min_entries=1, max_entries=20)
    token_serial = FormField(Token_serialForm)


class RenewForm(Form):
    """  Form for admin to add or edit a passport details """
   
    quota = QuerySelectField('Select Quota', query_factory=lambda: Quota.query.all(), get_label="quota_reference")
    new_issue_date = DateField('Expiry Date ', format='%Y-%m-%d')
    new_expiry_date  = DateField('Issue Date ', format='%Y-%m-%d') 
    submit = SubmitField('Submit')

class QuotaRenewForm(FlaskForm):
    renew = FormField(RenewForm)
    quota = FormField(QuotaForm)

   

class FolderForm(FlaskForm):
    """ This form helps add folder and categories"""
    date_created =  DateField('Date created', format='%Y-%m-%d')
    date_modified= DateField('Deleted modified ', format='%Y-%m-%d')
    folder_name = StringField('Create Folder name',validators=[DataRequired()])
    categories = SelectField(u'Select type of folder', choices=[('Litigations', 'Litigations'), ('Immigrations', 'Immigrations'),  ('Properties', 'Properties'),  ('Office Case', 'Office Case'),  ('Special Case', 'Special Case') ])
    submit = SubmitField('Submit')

    
 
class FileForm(FlaskForm):
    """ This form helps add files, name and tags"""
    date_created =  DateField('Date created', format='%Y-%m-%d')
    date_modified= DateField('Deleted modified ', format='%Y-%m-%d')
    file_document = StringField('File name',validators=[DataRequired()])
    tags = SelectField(u'Select tags', choices=[('Litigations', 'Litigations'), ('Immigrations', 'Immigrations'),  ('Properties', 'Properties'),  ('Office Case', 'Office Case'),  ('Special Case', 'Special Case') ])
    desc = TextAreaField('File Details')
    submit = SubmitField('Submit')   