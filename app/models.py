import os
import string
import calendar
import pathlib
from time import time
from hashlib import md5
from datetime import datetime, date
from datetime import date, timedelta
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


class Vendor(db.Model):
    
    __tablename__ = 'vendors'
    
    id = db.Column(db.Integer, primary_key=True)
    accountid = db.Column(db.String(120), index=True)
    phone_number=db.Column(db.String(16), index=True)
    company = db.Column(db.String(120), index=True)
    industry = db.Column(db.String(120), index=True)
    company_address  = db.Column(db.String(120), index=True)
    company_email = db.Column(db.String(120), index=True)
    city = db.Column(db.String(30), index=True, default = 'Ikeja')
    state =db.Column(db.String(20), index=True, default='Lagos')
    country = db.Column(db.String(120), index=True, default='Nigeria')
    postal_code = db.Column(db.String(20))
    logo_file = db.Column(db.String(120), nullable=False, default='default.jpg')
    contact_person = db.Column(db.String(120), index=True)
    contact_phone = db.Column(db.String(120), index=True)
    website = db.Column(db.String(120), index=True)

    #  we define relationships for companies anf all others
    user = db.relationship('User', backref='vendor', lazy='dynamic')
    account = db.relationship('Account', backref='vendor', lazy='dynamic')    
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Vendor('{self.phone_number}', '{self.accountid}', \
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
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    email = db.Column(db.String(120), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=True)
    birthday = db.Column(db.DateTime, default=datetime.utcnow)
    gender = db.Column(db.String(120), index=True)
    image_file = db.Column(db.String(120), default='default.jpg')
    active = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    # Vendor needs to be defineds on all tables 
    accountid = db.Column(db.String(120), index=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=True)
    # Messaging relationship to users
    messages = db.relationship('Message', backref='user', lazy='dynamic')
    teamates = db.relationship('Teamate', backref='user', lazy='dynamic')
    # recipients = db.relationship('Recipient', backref='user', lazy='dynamic')
    recipients = db.relationship('Recipient', backref='user', lazy='dynamic')
    usergroups = db.relationship('Usergroup', backref='user', lazy='dynamic')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    

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
        
    def get_vendor(self):
        return self.vendor_id


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




    
    

    
