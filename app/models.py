import os
import string
import calendar
import pathlib
from time import time
from hashlib import md5
from datetime import datetime, date
from datetime import date, timedelta
import dateutil.relativedelta
import dateutil.parser
import dateutil.rrule
from math import log2
from pathlib import Path
from decimal import Decimal
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin, AnonymousUserMixin
from app import db, login
from sqlalchemy.orm import sessionmaker
import emoji


# Set up user_loader
@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Chamber(db.Model):
    
    __tablename__ = 'chambers'
    
    id = db.Column(db.Integer, primary_key=True)
    phone_number=db.Column(db.String(16), index=True)
    accountid = db.Column(db.String(120), index=True)
    company = db.Column(db.String(120), index=True)
    industry = db.Column(db.String(120), index=True)
    company_address  = db.Column(db.String(120), index=True)
    company_email = db.Column(db.String(120), index=True)
    city = db.Column(db.String(30), index=True, default = 'Ikeja')
    state =db.Column(db.String(20), index=True, default='Lagos')
    country = db.Column(db.String(120), index=True, default='United Kingdom')
    postal_code = db.Column(db.String(20))
    logo_file = db.Column(db.String(120), nullable=False, default='default.jpg')
    contact_person = db.Column(db.String(120), index=True)
    contact_phone = db.Column(db.String(120), index=True)
    website = db.Column(db.String(120), index=True)
    is_immigration = db.Column(db.Integer)
    is_probate = db.Column(db.Integer)
    is_entertainment = db.Column(db.Integer)
    is_realestate = db.Column(db.Integer)
    is_services = db.Column(db.Integer)
    is_Iproperty = db.Column(db.Integer)
    is_Billings = db.Column(db.Integer)
    #  we define relationships for companies anf all others
    user = db.relationship('User', backref='chamber', lazy='dynamic')

    account = db.relationship('Account', backref='chamber', lazy='dynamic')
    
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Chamber('{self.phone_number}', '{self.accountid}', \
        '{self.logo_file}','{self.timestamp}', '{self.company}')"
        
        

class Permission:
        
    VIEW = 1
    ACCOUNT = 2
    ADMIN = 4
    MANAGE = 8
    SUPER_ROLE = 16      

       
       
class Role(db.Model):
    
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    permissions = db.Column(db.Integer)
    user = db.relationship('User', backref='role', lazy='dynamic')        
  
    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:            
            self.permissions = 0    
   
            
    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm
            
    def reset_permissions(self):
        self.permissions = 0
    
    def has_permission(self, perm):
        return self.permissions & perm == perm
    
    def __repr__(self):
        return '<Role %r>' % self.name    
            


class Teamate(db.Model):    
        
    __tablename__ = 'teamates'
        
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120))
    name = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  
    
    def __repr__(self):
        return '<Teamate %r>' % self.name   

    


     

class User(db.Model, UserMixin):
        
    __tablename__ = 'users'
        
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=True)
    chamber_id = db.Column(db.Integer, db.ForeignKey('chambers.id'), nullable=True)
    email = db.Column(db.String(120), unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    birthday = db.Column(db.DateTime, default=datetime.utcnow)
    gender = db.Column(db.String(120), index=True)
    image_file = db.Column(db.String(120), default='default.jpg')
    active = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(128))
    initiator = db.Column(db.Integer, default=0)
    invitee = db.Column(db.Integer, default=0)
    invitee_name = db.Column(db.String(120))
    confirmed = db.Column(db.Boolean, default=False)
    # Chamber needs to be defineds on all tables 
    accountid = db.Column(db.String(120), index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    timesend = db.Column(db.DateTime, default=datetime.utcnow)
    # Messaging relationship to users
    messages = db.relationship('Message', backref='user', lazy='dynamic')
    teamates = db.relationship('Teamate', backref='user', lazy='dynamic')
    # recipients = db.relationship('Recipient', backref='user', lazy='dynamic')
    recipients = db.relationship('Recipient', backref='user', lazy='dynamic')
    usergroups = db.relationship('Usergroup', backref='user', lazy='dynamic')
    

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_accountant(self):
        return self.can(Permission.ACCOUNT)
    
    def is_administrator(self):
        return self.can(Permission.ADMIN)
    
    def is_manager(self):
        return self.can(Permission.MANAGE)
    
    def is_superUser(self):
        return self.can(Permission.SUPER_ROLE)
            
      
    def get_id(self):        
        return self.id

    def is_active(self):
        return  True

    def activate_user(self):
        self.confirmed = True

    def get_username(self):
            return self.username
        
    def get_chamber(self):
        return self.chamber_id


    # This method confirms every registration and activate every account opened
    def get_confirmation_token(self, expires_sec=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True
    

    #Expiry link for the token is set @ 5 Minutes 
    def get_reset_token(self, expires_sec=2000):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')
    
    @password.setter
    def password(self, password):
        """  Set password to a hashed password   """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """ Check if hashed password matches actual password """
        return check_password_hash(self.password_hash, password)
    

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        
    @property  
    def label(self):
        label = ("{} {}".format(self.first_name, self.last_name))        
        return(label)


    def __repr__(self):
            return '<User {}>'.format(self)
        
        
        
class AnonymousUser(AnonymousUserMixin):
    
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False
    
    def is_accountant(self):
        return False
    
    def is_administrator(self):
        return False
    
    def is_manager(self):
        return False
        
    def is_superUser(self):
        return False

login.anonymous_user = AnonymousUser


class Employee(db.Model):
    
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    accountid = db.Column(db.Integer)
    email = db.Column(db.String(120), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    label = db.Column(db.String(120), index=True)
    phone_number=db.Column(db.String(16), index=True)
    gender = db.Column(db.String(60), index=True)
    address=db.Column(db.String(120), index=True)
    city = db.Column(db.String(30), index=True)
    state = db.Column(db.String(20), index=True) 
    country = db.Column(db.String(20), index=True)   
    birthday = db.Column(db.DateTime)
    date_of_employment = db.Column(db.DateTime)
    passport_pic = db.Column(db.String(50), default='default.png')
    deleted_at = db.Column(db.DateTime, nullable=True)
    expat_id = db.Column(db.String(60), index=True)
    # Here we define the relationship<---------------------------->
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    lap_id = db.Column(db.Integer, db.ForeignKey('laps.id'))
    # folder_id = db.Column(db.Integer, db.ForeignKey('folders.id'))
    is_notified = db.Column(db.Boolean, default=False)
    is_immigration = db.Column(db.Boolean, default=False)
    is_probate = db.Column(db.Boolean, default=False)
    is_ent = db.Column(db.Boolean, default=False)
    is_realestate = db.Column(db.Boolean, default=False)
    is_services = db.Column(db.Boolean, default=False)
    is_Iproperty = db.Column(db.Boolean, default=False)
    is_Billings = db.Column(db.Boolean, default=False)
    create_folder = db.Column(db.Boolean, default=False)
    # Here we define further<------------------------------------->
    emergencies = db.relationship('Emergency', backref='employee', lazy='dynamic')
    dependents = db.relationship('Dependent', backref='employee', lazy='dynamic')
    folders = db.relationship('Folder', backref='employee', lazy='dynamic')
    passports = db.relationship('Passport', backref='employee', lazy='dynamic')
    cerpacs = db.relationship('Cerpac', backref='employee', lazy='dynamic')
    quotas = db.relationship('Quota', backref='employee', lazy='dynamic')
    realestates = db.relationship('RealEstate', backref='employee', lazy='dynamic')
    account = db.relationship('Account', backref='employee', lazy='dynamic')
    recipients = db.relationship('Recipient', backref='employee', lazy='dynamic')
    # We set properties for actual age from Birthday<--------------->
    get_age = db.Column(db.DateTime)
    get_bday = db.Column(db.DateTime)
    get_anny = db.Column(db.DateTime)
    employment_age =  db.Column(db.DateTime)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
  
    def __repr__(self):
        return '<Employee {}>'.format(self)

  
       

    @property
    def get_age(self):

        today = date.today()
        try:
            birthday = (self.birthday).replace(year = today.year)

    # raised when birth date is February 29 
    # and the current year is not a leap year 
        except ValueError:
            birthday = (self.birthday).replace(year = today.year, 
                    month = (self.birthday).month + 1, day = 1) 
            #print(birthday)
        if birthday.date()  > today:
            age =  today.year -(self.birthday).year - 1
            return (age)

        else: 
            age = today.year - (self.birthday).year
            return (age) 

    
    @property
    def get_anny(self):
        today = datetime.now()
        anny = (self.date_of_employment).replace(year = today.year) 
        diff = (anny - today).days
        check = diff+1
        flag = "check later"
        if check < 0 :
            annys = (self.date_of_employment).replace(year = today.year + 1) 
            flag =  annys.strftime('%d,%B, %Y')           
        elif check ==0 and check < 1:
            flag = (emoji.emojize("#Happy Work Anniversary! :birthday_cake:",variant="emoji_type"))
        elif check ==1:
            flag = (emoji.emojize("#Work Anniversary coming! :thumbs_up:",variant="emoji_type"))
        elif check >1 and check < 8:
            flag =  ( "# {}".format(check) + " Days Left! " + " \U0001F389 " )
        elif check > 8 and check <=30:
            flag= ("# {}" .format(check) + " Days Left " + "\U0001F44C " )          
        else:
            flag = anny.strftime('%d,%b, %Y')   
        return (flag, check)

    @property
    def get_bday(self):

        today = datetime.now()
        #time =  self.expired_date - datetime.now()
        bday = (self.birthday).replace(year = today.year) 
        #print(bday)
        #bday = date(today.year,6,30)
        diff = (bday - today).days
        diffu = diff+1
        flag = "check later"
        if diffu < 0 :
            bdays = (self.birthday).replace(year = today.year + 1) 
            flag =  bdays.strftime('%d,%B, %Y')
            output =0
        elif diffu ==0 and diffu <1:
            flag = (emoji.emojize("#Bday Hurray! :birthday_cake:",variant="emoji_type"))
      

        elif diffu ==1:
                flag = (emoji.emojize("#Bday Tomorrow! :thumbs_up:",variant="emoji_type"))
                

        elif diffu >1 and diffu < 8:
            flag =  ( "# {}".format(diffu) + " Days Left! " + " \U0001F389 " )
            

        elif diffu >8 and diffu <=30:
            flag= ("# {}" .format(diffu) + " Days Left " + "\U0001F44C " )
          
        else:
            flag = bday.strftime('%d,%b, %Y')   
        return (flag, diffu)
            
    @property    
    def renew_status(self):

        flag = 'Active'
        if self.remaining_days <= 410  and self.remaining_days > 365:
                flag = 'warning'
        elif self.remaining_days <=365 :
                flag = 'Expired'
        return(flag)
    
    @property    
    def label(self):
        label = ("{} {} ".format(self.first_name, self.last_name))        
        return(label)
    
    @property    
    def full_name(self):
        full_name = ("{} {}".format(self.first_name, self.last_name))        
        return(full_name)

  

"""Table for Dependent - 
Employee can have many Wife, Mother, Son and Children
relationship with Employee, 
wife Mother, Son , Daughter have many
Passport, Cerpac empoloyee """




class Emergency(db.Model):
    
        __tablename__ = 'emergencies'
        
        id = db.Column(db.Integer, primary_key=True) 
        name = db.Column(db.String(60), unique=True)
        phone = db.Column(db.String(16), index=True)
        relationship = db.Column(db.String(16), index=True)
        address = db.Column(db.String(200))
        accountid = db.Column(db.Integer, index=True)
        expat_id = db.Column(db.String(16), index=True)
        employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
        timestamp = db.Column(db.DateTime, default=datetime.utcnow)
        
        def __repr__(self):
            return '<Emergenncy {}>'.format(self.name)

class Dependent(db.Model):
    
        __tablename__ = 'dependents'
        
        id = db.Column(db.Integer, primary_key=True) 
        name = db.Column(db.String(60))
        email = db.Column(db.String(60))
        phone = db.Column(db.String(16), index=True)
        relationship = db.Column(db.String(16), index=True)
        birthday = db.Column(db.DateTime)
        gender = db.Column(db.String(60), index=True)
        accountid = db.Column(db.Integer, index=True)
        expat_id = db.Column(db.String(16), index=True)
        employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
        folders = db.relationship('Folder', backref='dependent', lazy='dynamic')
        passports = db.relationship('Passport', backref='dependent', lazy='dynamic')
        cerpacs = db.relationship('Cerpac', backref='dependent', lazy='dynamic')
        passport_pic = db.Column(db.String(50), default='default.png')
        timestamp = db.Column(db.DateTime, default=datetime.utcnow)
        
        def __repr__(self):
            return '<Dependent {}>'.format(self.name)



class Cerpac(db.Model):
    
        __tablename__ = 'cerpacs'
        
        id = db.Column(db.Integer, primary_key=True) 
        cerpac_issue_date = db.Column(db.DateTime)
        expired_date = db.Column(db.DateTime)
        remaining_days = db.Column(db.DateTime)
        cerpac_serial_no = db.Column(db.String(60))
        ccn_number = db.Column(db.String(60))
        cerpac_upload = db.Column(db.String(20), default='cerpac.jpg')
        # Above is for the forms 
        verified = db.Column(db.Boolean, default=False)
        renew_status = db.Column(db.Boolean)
        process_status = db.Column(db.Boolean, default=False)
        expat_id = db.Column(db.String(16), index=True)
        renew_id = db.Column(db.Integer, db.ForeignKey('renews.id'))
        dependent_id = db.Column(db.Integer, db.ForeignKey('dependents.id'))
        approve_id = db.Column(db.Integer, db.ForeignKey('approves.id'))
        pedal = db.Column(db.Integer)        
        employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
        accountid = db.Column(db.Integer, index=True)
        timestamp = db.Column(db.DateTime, default=datetime.utcnow)

                
        def __repr__(self):
             return '<Cerpac {}>'.format(self)
    
        @property
        def remaining_days(self):
            time =  self.expired_date - datetime.now()
            #print(self.expired_date)
            #print(self.cerpac_issue_date)
            #return (time).days
            return (time).days
            
        @property    
        def renew_status(self):
            flag = 'Active'
            if self.remaining_days <= 410  and self.remaining_days > 365:
                    flag = 'warning'
            elif self.remaining_days <=365 :
                    flag = 'Expired'
            return(flag)

        @property
        def days_to_expiry(self):
            return (self.cerpac_exp_date - datetime.now()).days


class Company(db.Model):
    
        __tablename__ = 'companies'
        
        id = db.Column(db.Integer, primary_key=True) 
        company_name= db.Column(db.String(60), unique=True)
        company_address = db.Column(db.String(200))
        rcc_number = db.Column(db.String(50))
        city= db.Column(db.String(60))
        state =db.Column(db.String(60))
        postal_code = db.Column(db.String(60))
        country =  db.Column(db.String(60))       
        contact_person =  db.Column(db.String(60))       
        company_email = db.Column(db.String(120), index=True)
        contact_number = db.Column(db.String(120), index=True)
        company_number = db.Column(db.String(120), index=True)
        nature=  db.Column(db.String(120), index=True)
        logo_image = db.Column(db.String(30), default='default.png')
        accountid = db.Column(db.Integer, index=True)
        quota = db.relationship('Quota', backref='company',lazy='dynamic')
        employee = db.relationship('Employee', backref='company', lazy='dynamic')
        folders = db.relationship('Folder', backref='company', lazy='dynamic')
        Detail = db.relationship('Detail', backref='company', lazy='dynamic')
        account = db.relationship('Account', backref='company', lazy='dynamic')
        recipients = db.relationship('Recipient', backref='company', lazy='dynamic')
        deleted_at = db.Column(db.DateTime, nullable=True)
        is_notified = db.Column(db.Boolean, default=False)
        is_immigration = db.Column(db.Boolean, default=False)
        is_probate = db.Column(db.Boolean, default=False)
        is_ent = db.Column(db.Boolean, default=False)
        is_realestate = db.Column(db.Boolean, default=False)
        is_services = db.Column(db.Boolean, default=False)
        verified = db.Column(db.Boolean, default=False)
        is_Iproperty = db.Column(db.Boolean, default=False)
        is_Billings = db.Column(db.Boolean, default=False)
        timestamp = db.Column(db.DateTime, default=datetime.utcnow)
        
        

        def __repr__(self):
            return '<Company {}>'.format(self)
       
        @property    
        def label(self):
            label = ("{} {} ".format(self.company_name, self.state))        
            return(label)

class Quota(db.Model):
    
        __tablename__ = 'quotas'
        
        id = db.Column(db.Integer, primary_key=True)
        no_of_positions = db.Column(db.Integer)
        effective_date =db.Column(db.DateTime)
        quota_exp_date = db.Column(db.DateTime)
        quota_upload = db.Column(db.String(30),  default='quota.jpg')
        quota_reference = db.Column(db.String(60), unique=True)
        remaining_days = db.Column(db.DateTime)
        # add 3 more lines to describe the quota 
        verified = db.Column(db.Boolean, default=False)
        application_id = db.Column(db.String(160))
        type_of_application = db.Column(db.String(160))
        current_status = db.Column(db.String(160))
        approval_date = db.Column(db.String(160))
        # complete lists 
        renew_status = db.Column(db.Boolean, default=False)
        process_status = db.Column(db.Integer, default=0, nullable=False)
        approval_status = db.Column(db.Integer, default=0, nullable=False)
        approval_count = db.Column(db.Integer, default=0)
        employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
        expat_id = db.Column(db.String(16), index=True)
        renew_id = db.Column(db.Integer, db.ForeignKey('renews.id'))
        approve_id = db.Column(db.Integer, db.ForeignKey('approves.id'))
        pedal = db.Column(db.Integer)
        #renews = db.relationship('Renew', backref='quota',lazy='dynamic')
        # here we define a relationship
        company_id =  db.Column(db.Integer, db.ForeignKey('companies.id'))
        lap_id = db.Column(db.Integer, db.ForeignKey('laps.id'))
        token_serials = db.relationship('Token_serial', backref='quota',lazy='dynamic')
        accountid = db.Column(db.Integer, index=True)
        timestamp = db.Column(db.DateTime, default=datetime.utcnow)

        
        def __repr__(self):
            return '<Quota {}>'.format(self)

        @property
        def remaining_days(self):
            time =  self.quota_exp_date - datetime.now()
            return (time).days
            
        @property    
        def renew_status(self):
            flag = 'Active'
            if self.remaining_days <= 410  and self.remaining_days > 365:
                    flag = 'warning'
            elif self.remaining_days <=365 :
                    flag = 'Expired'
                    # self.process_status = 0
                    # self.approval_status = 0

            return(flag)

     

class Passport(db.Model):
        __tablename__ = 'passports'
        id = db.Column(db.Integer, primary_key=True) 
        nationality = db.Column(db.String(60))
        passport_no = db.Column(db.String(16), unique=True)
        renew_status = db.Column(db.Boolean, default=False)
        process_status = db.Column(db.Boolean, default=False)
        verified = db.Column(db.Boolean, default=False)
        remaining_days = db.Column(db.DateTime)
        passport_exp_date = db.Column(db.DateTime)
        passport_issue_date = db.Column(db.DateTime)
        expat_id = db.Column(db.String(16), index=True)
        count_down = db.Column(db.DateTime)
        accountid = db.Column(db.Integer, index=True)
        renew_id = db.Column(db.Integer, db.ForeignKey('renews.id'))
        approve_id = db.Column(db.Integer, db.ForeignKey('approves.id'))
        pedal = db.Column(db.Integer)
        employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
        dependent_id = db.Column(db.Integer, db.ForeignKey('dependents.id'))
        timestamp = db.Column(db.DateTime, default=datetime.utcnow)
        
        def __repr__(self):
            return '<Passport {}>'.format(self)
        def __repr__(self):
            return f"Passport('{self.nationality}', '{self.passport_no}', \
        '{self.renew_status}','{self.process_status}', '{self.remaining_days}',\
        '{self.remaining_days}', '{self.passport_exp_date}', '{self.passport_issue_date}')"
        
        @property
        def remaining_days(self):
            #time =  self.passport_exp_date - self.passport_issue_date
            time = self.passport_exp_date - datetime.now()
            return (time).days
            
        @property    
        def renew_status(self):
            flag = 'Active'
            if self.remaining_days <= 425  and self.remaining_days > 365:
                    flag = 'warning'
            elif self.remaining_days <=365 :
                    flag = 'Expired'
            return(flag)

        @property
        def count_down(self):
            cont = self.passport_exp_date - datetime.date.today()
            print(cont)
            return(cont).days


            
""" This is a test form for child and parent database and reltionship"""

class Token_serial(db.Model):
    """Stores races."""
    
    __tablename__ = 'token_serials'
    
    id = db.Column(db.Integer, primary_key=True)
    serial_no = db.Column(db.String(60))
    quota_id = db.Column(db.Integer, db.ForeignKey('quotas.id'))
    accountid = db.Column(db.Integer, index=True)
    laps = db.relationship('Lap', backref='token_serial',lazy='dynamic')
    accountid = db.Column(db.Integer, index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Token_serial {}>'.format(self)

class Lap(db.Model):
    """stores  quota positions"""
    
    __tablename__ = 'laps'
       
    id = db.Column(db.Integer, primary_key=True)
    quota_id = db.Column(db.Integer, db.ForeignKey('quotas.id'))
    token_serial_id = db.Column(db.Integer, db.ForeignKey('token_serials.id'))
    runner_name = db.Column(db.String(100))
    accountid = db.Column(db.Integer, index=True)
    employee_name = db.Column(db.String(100))
    passport_pic = db.Column(db.String(60))
    expat_id = db.Column(db.String(60), index=True)
    quota_id = db.Column(db.Integer, index=True)
    #  please change the stuff
    employees = db.relationship('Employee', backref='laps', lazy='dynamic')
    quotas = db.relationship('Quota', backref='laps',lazy='dynamic')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):      
        return '<Lap {}>'.format(self)


class Renew(db.Model):

    __tablename__ = 'renews' 
    id = db.Column(db.Integer, primary_key=True)
    quotas = db.relationship('Quota', backref='renews',lazy='dynamic')
    passports = db.relationship('Passport', backref='renews',lazy='dynamic')
    cerpacs = db.relationship('Cerpac', backref='renews',lazy='dynamic')
    date_renewed = db.Column(db.DateTime)
    accountid = db.Column(db.Integer, index=True)
    pedal = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
           
    def __repr__(self):
        
        return '<Renew {}>'.format(self)

class Approve(db.Model):
    
    __tablename__ = 'approves'
     
    id = db.Column(db.Integer, primary_key=True)
    quotas = db.relationship('Quota', backref='approves',lazy='dynamic')
    passports = db.relationship('Passport', backref='approves',lazy='dynamic')
    cerpacs = db.relationship('Cerpac', backref='approves',lazy='dynamic')
    new_issue_date = db.Column(db.DateTime)
    new_expiry_date = db.Column(db.DateTime)
    date_approved = db.Column(db.DateTime)
    accountid = db.Column(db.Integer, index=True)
    pedal = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
        
    def __repr__(self):
        return '<Approve {}>'.format(self)



class Folder(db.Model):

    __tablename__ = 'folders'
    
    id = db.Column(db.Integer, primary_key=True)
    folder_name =  db.Column(db.String(60), nullable=False)
    categories =  db.Column(db.String(80))
    folder_size =  db.Column(db.String(80))
    folder_path = db.Column(db.String(400))
    date_created =  db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    accountid = db.Column(db.Integer, index=True)
    expat_id = db.Column(db.String(16), index=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    dependent_id = db.Column(db.Integer, db.ForeignKey('dependents.id'))
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    files = db.relationship('File', backref='folders',lazy='dynamic')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Folder {}>'.format(self)
        # return f"Folder('{self.folder_name}', '{self.categories}', \
        # '{self.folder_size}','{self.date_created}', '{self.date_deleted}')"


    @property
    def folder_size(self):
        cabinet = os.path.join(current_app.root_path,'static/cabinet')
        file_path = str((pathlib.Path(cabinet, self.folder_name))).strip()
        # file_path = pathlib.Path(cabinet, self.folder_name)
        if os.path.exists(file_path) or os.path.exists:
            total_size = os.path.getsize(file_path)
            for item in os.listdir(file_path):
                itempath = os.path.join(file_path, item)
                if os.path.isfile(itempath):
                    total_size += os.path.getsize(itempath)
                elif os.path.isdir(itempath):
                    total_size += folder_size(itempath)
        # Calculate the values from bytes to  Kb, Mb and Gb
            units = ("B", "KiB", "MiB", "GiB", "TiB", "PiB",  "EiB", "ZiB", "YiB") 
            flag ="Empty Folder"
            if total_size > 0:
                scaling = round(log2(total_size)*4)//40
                scaling = min(len(units)-1, scaling)
                cap =  total_size/(2**(10*scaling)), units[scaling]
                flag = ("%.3f %s" % cap)
            elif total_size == None:
                flag = "Empty Folder"
            return flag


        
class File(db.Model):
    
    __tablename__ = 'files'
    
    id = db.Column(db.Integer, primary_key=True)
    file_document =  db.Column(db.String(60))
    tags =  db.Column(db.String(80))
    date_created =  db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    ext = db.Column(db.String(10))
    desc = db.Column(db.String(120))
    accountid = db.Column(db.Integer, index=True)
    folder_id = db.Column(db.Integer, db.ForeignKey('folders.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    

    def __repr__(self):

                
        return '<File {}>'.format(self)



class RealEstate(db.Model):

    __tablename__ = 'realestates'
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(60), nullable=False)
    description = db.Column(db.String, nullable=False)
    location = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    country = db.Column(db.String(120))
    transaction_status = db.Column(db.String(120)) # Sales or Lease/Rent
    accountid = db.Column(db.Integer, index=True)
    ownership = db.Column(db.String(120)) #commercial,  or private
    typeof = db.Column(db.String(120)) # Agricultural, resident, service-purpose, special-purpose, Industrial
    search_status = db.Column(db.Boolean, default=False) #Search CofO
    value = db.Column(db.Float, nullable=False) #estimated Value
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    real_estate_transactions = db.relationship('RealEstateTransactions', backref='folders',lazy='dynamic')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
             
        return '<RealEstate {}>'.format(self)



class RealEstateTransactions(db.Model):

    __tablename__ = 'realestates_transaction'
    
    id = db.Column(db.Integer, primary_key=True)
    accountid = db.Column(db.Integer, index=True)
    name =  db.Column(db.String(60), nullable=False)
    description = db.Column(db.String, nullable=False)
    typeof = db.Column(db.String(120)) #rent, sold or lease
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    renewal_date = db.Column(db.DateTime, default=datetime.utcnow)
    expiry_date =  db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    realestate_id = db.Column(db.Integer, db.ForeignKey('realestates.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    

    def __repr__(self):
             
        return '<RealEstateTransactions {}>'.format(self)

        
class Probate(db.Model):
    
    __tablename__ = 'probates'
    
    id = db.Column(db.Integer, primary_key=True)    
    name =  db.Column(db.String(60), nullable=False )
    will_satus = db.Column(db.Boolean, default=False)
    executors = db.Column(db.String(120))
    nextofkins= db.Column(db.String(120))
    accountid = db.Column(db.Integer, index=True)
    # probateassets = db.relationship('Probateasset', backref='probate',lazy='dynamic')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

  
    def __init__(self, name, will_satus, executors, nextofkins):
        self.name=name
        self.will_status=will_satus
        self.executors=executors
        self.nextofkins=nextofkins


class Probateassets(db.Model):

     __tablename__ = 'probateassets'
     id = db.Column(db.Integer, primary_key=True) 
     name =  db.Column(db.String(60), nullable=False)
     value = db.Column(db.Float, nullable=False)
     accountid = db.Column(db.Integer, index=True)
    #  probate_id = db.Column(db.Integer, db.ForeignKey('probates.id'))
     timestamp = db.Column(db.DateTime, default=datetime.utcnow)


     def __init__(self, name, value):
        self.name=name
        self.value=value

class Iproperty(db.Model):

    __tablename__ = 'Iproperties'
    id = db.Column(db.Integer, primary_key=True) 
    name =  db.Column(db.String(60), nullable=False)
    value = db.Column(db.Float, nullable=False)
    accountid = db.Column(db.Integer, index=True)



    def __repr__(self):
        return '<Iproperty {}>'.format(self)



class Services(db.Model):

    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True) 
    name =  db.Column(db.String(60), nullable=False)
    description =  db.Column(db.String(60), nullable=False)
    value = db.Column(db.Float, nullable=False)
    accountid = db.Column(db.Integer, index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    

    def __repr__(self):        
        return '<Services {}>'.format(self)



class Invoice(db.Model):
        
    __tablename__ = 'invoices'
       
    id = db.Column(db.Integer, primary_key=True)    
    items = db.Column(db.String(60)) 
    description = db.Column(db.String(60)) 
    qty =db.Column(db.Float)  #  
    cost =db.Column(db.Float)
    accountid = db.Column(db.Integer, index=True)
    invoice_id = db.Column(db.String(60))#
    # Relationship-------------------------------------------
    Detail_id = db.Column(db.Integer, db.ForeignKey('details.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
 
    def __repr__(self):        
        return '<Invoice {}>'.format(self)
    
    
    
class Detail(db.Model):
    
    __tablename__ = 'details'
    # <-------------------------------------------------------------------->
    id = db.Column(db.Integer, primary_key=True)    
    invoiceID = db.Column(db.String(60))
    invoiceDate =db.Column(db.DateTime, default=datetime.utcnow) 
    expiryDate =db.Column(db.DateTime, default=datetime.utcnow) 
    billingPeriod = db.Column(db.String(60))
    billingAddress = db.Column(db.String(120))
    clientAddress = db.Column(db.String(120))
    contactPerson = db.Column(db.String(60))
    contactEmail = db.Column(db.String(60))
    paymentStatus = db.Column(db.Boolean, default=False)
    paymentMade = db.Column(db.Float)
    balance = db.Column(db.Float)
    paymentMethod = db.Column(db.String(60))    
    otherInfo = db.Column(db.String(60))        
    #//<----Figures and Floats//--------------------------------------------->    
    tax = db.Column(db.Float) 
    discount= db.Column(db.Float)
    discountAmt =db.Column(db.Float)
    taxAmt = db.Column(db.Float )
    subTotal =db.Column(db.Float)  
    grandTotal =db.Column(db.Float)
    accountid = db.Column(db.Integer, index=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'))        
    #//<--Relationship//--------------------------------------------------------->
    invoice = db.relationship('Invoice', backref='Detail', lazy='dynamic')
    account = db.relationship('Account', backref='Detail', lazy='dynamic')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)    
    #<---------------------------------------------------------------------------> 
        
    def __repr__(self):        
        return '<Detail {}>'.format(self)
    
    # @property
    # def paymentStatus(self):        
    #     today = date.today()
    #     if not self.expiryDate < today:           
    #        flag = "Active"
    #     else:
    #         flag = "Amount Due"           
    #     return (flag)

    



class Payment(db.Model):
        
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True) 
    amount = db.Column(db.Float)
    description = db.Column(db.String(60))
    paymentType = db.Column(db.String(60)) 
    
    """ we declare relationship of one-to-many"""        
    account = db.relationship('Account', backref='Payment', lazy='dynamic')
    detail = db.relationship('Detail', backref='Payment', lazy='dynamic')    
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallets.id'))  
    accountid = db.Column(db.Integer, index=True)    
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Payment {}>'.format(self)
    
    
    
    


    
class Wallet(db.Model):
        
    __tablename__ = 'wallets'
        
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(60))
    amount = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    accountid = db.Column(db.Integer, index=True)
    # //Relationship
    payment = db.relationship('Payment', backref='Wallet', lazy='dynamic')
    
    
    def __repr__(self):
        return 'Wallet {}>'.format(self)  
    
    
class Account(db.Model):
        
    __tablename__ = 'accounts'
        
    id = db.Column(db.Integer, primary_key=True)
    TransactionDate = db.Column(db.DateTime, default=datetime.utcnow)
    valueDate = db.Column(db.DateTime, default=datetime.utcnow)
    paymentDate = db.Column(db.DateTime, default=datetime.utcnow)
    debit = db.Column(db.Float, nullable=False, default = 0.00)
    credit = db.Column(db.Float, nullable=False, default = 0.00)
    balance = db.Column(db.Float, nullable=False)
    reference = db.Column(db.String(60))
    remark = db.Column(db.String(120))
    accountid = db.Column(db.Integer, index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    # Relationship with chamber, payment, detauil, employee, company
    chamber_id = db.Column(db.Integer, db.ForeignKey('chambers.id'))
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'))
    detail_id = db.Column(db.Integer, db.ForeignKey('details.id'))
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    
    def __repr__(self):
        return 'Account {}>'.format(self)
        
        
class Tax(db.Model):
        
    __tablename__ = 'taxes'
        
    id = db.Column(db.Integer, primary_key=True) 
    name =  db.Column(db.String(60), nullable=False, unique=True)
    description = db.Column(db.String(60), nullable=False, unique=True)
    percentage = db.Column(db.Float, nullable=False)
    accountid = db.Column(db.Integer, index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    
    def __repr__(self):
        return 'Tax {}>'.format(self)
            

"""messaging model"""

class Message(db.Model):
           
    __tablename__ = 'messages'
           
    id = db.Column(db.Integer, primary_key=True) 
    subject = db.Column(db.String(160), nullable=False)
    sender_name = db.Column(db.String(160))
    message_body =db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    expiry_date = db.Column(db.DateTime)
    is_reminder = db.Column(db.Boolean, default=False)
    next_reminder_date = db.Column(db.DateTime)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    accountid = db.Column(db.Integer, index=True)
    # User Relationship    
    frequency_id = db.Column(db.Integer, db.ForeignKey('frequencies.id'))
    recipients = db.relationship("Recipient", back_populates="messages") 
 
    def __repr__(self):
        return 'Message {}>'.format(self)
    
    def expiry_date(self):
        tick_date = self.timestamp + timedelta(30)        
        return tick_date
    

    
    
class Group(db.Model):
    
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=False)
    usergroups = db.relationship('Usergroup', backref='group', lazy='dynamic')
    recipients = db.relationship('Recipient', backref='group', lazy='dynamic')
    
    def __repr__(self):
        return ' Group {}>'.format(self)    
    
    
class Recipient(db.Model):
           
    __tablename__ = 'recipients'
    
    id = db.Column(db.Integer, primary_key=True) 
    is_read =  db.Column(db.Boolean, default=False)
    is_stared =  db.Column(db.Boolean, default=False)
    is_checked =  db.Column(db.Boolean, default=False)
    is_trashed =  db.Column(db.Boolean, default=False)
    is_draft =  db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=True)
    user_id  = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=True)    
    recipient_id = db.Column(db.Integer)
    email_id = db.Column(db.Integer, db.ForeignKey('messages.id'))
    messages = db.relationship("Message", back_populates="recipients", uselist=False)
    categories = db.Column(db.String(60), nullable=False) 
    name = db.Column(db.String(60), nullable=False,) 
    email = db.Column(db.String(60), nullable=False,) 
    

    def __repr__(self):
        return 'Recipient {}>'.format(self)
    

    def timestamp(self):        
        # time = self.timestamp
        if (datetime.utcnow() - self.timestamp) > timedelta(1):
            time  = self.timestamp.strftime('%b %d')
        else:
            time  = self.timestamp.strftime('%I:%M:%S %p')
        return time
            
        

class Frequency(db.Model):
    
    __tablename__ = 'frequencies'
    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(60), nullable=False, unique=True)
    frequency = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=False)
    messages =  db.relationship('Message', backref='Frequency', lazy='dynamic') 
    
        
    def __repr__(self):
        return ' Frequency {}>'.format(self)
    
    
    
class Usergroup(db.Model):
    
    __tablename__ = 'usergroups'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=False) 
    # relationship
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    
    
    def __repr__(self):
        return ' Usergroup {}>'.format(self)
    
    
    

    
