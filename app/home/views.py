import re
from app.home import bp
from flask import abort, render_template,flash, redirect, url_for, request
from flask_login import current_user, login_required
# from flask_user import current_user, login_required, roles_required, UserManager, UserMixin
from sqlalchemy import func, and_
from datetime import datetime, date, timedelta
from app.home.forms import LapForm, MainForm
from app import db, session, sessionmaker
from app.auth.email import  send_set_email
from app.models import  Employee, Cerpac, Company, Emergency, \
Passport, Quota, User, Token_serial, Lap, Renew, Approve, Folder, File 


 #add admin dashboard view
@bp.route('/dashboard')
@login_required
def admin_dashboard():
    
    if not current_user.role.permissions == 31:
    
        employee = db.session.query(Employee.id).filter(Employee.accountid == current_user.chamber_id).count()
        employee_list = Employee.query.filter(Employee.accountid == current_user.chamber_id).limit(5).all()
        passport = db.session.query(Passport.id).filter(Passport.accountid == current_user.chamber_id).count()
        passport_list = Passport.query.filter(Passport.accountid == current_user.chamber_id).all()
        cerpac = db.session.query(Cerpac.id).filter(Cerpac.accountid == current_user.chamber_id).count()
        cerpac_list = Cerpac.query.filter(Cerpac.accountid == current_user.chamber_id).limit(5).all()
        quota = db.session.query(Quota.id).filter(Quota.accountid == current_user.chamber_id).count()
        quota_list = Quota.query.filter(Quota.accountid == current_user.chamber_id).limit(5).all()
        positions = db.session.query(Lap.id).filter(Lap.accountid == current_user.chamber_id).count()
        position_not_enrolled = db.session.query(Lap).filter(Lap.employee_name == None ).filter(Lap.accountid == current_user.chamber_id).count()
        position_enrolled = db.session.query(Lap).filter(Lap.employee_name != None).filter(Lap.accountid == current_user.chamber_id).count()
        # Percentage for position available and those not available is calculated below
        
        position_list=Lap.query.order_by(Lap.timestamp).filter(Lap.accountid == current_user.chamber_id).limit(2).all()
        company_list=Company.query.filter(Company.accountid == current_user.chamber_id).all()
        companies = db.session.query(Company.id).filter(Company.accountid == current_user.chamber_id).count()
        emergency = db.session.query(Emergency).filter(Emergency.accountid == current_user.chamber_id).count()
        approval = db.session.query(Approve.id).filter(Approve.accountid == current_user.chamber_id).count()
        renew = db.session.query(Renew.id).filter(Renew.accountid == current_user.chamber_id).count()
        folders = db.session.query(Folder.id).filter(Folder.accountid == current_user.chamber_id).count()
        categories = db.session.query(Folder.categories).filter(Folder.accountid == current_user.chamber_id).distinct().all()
        files = db.session.query(File.id).filter(File.accountid == current_user.chamber_id).count()
        if  position_enrolled == 0:
            percentage = 0
        else:
            percentage = ((position_not_enrolled)/(position_enrolled)) * 100
    else:    
        employee = db.session.query(Employee.id).count()
        employee_list = Employee.query.limit(5).all()
        passport = db.session.query(Passport.id).count()
        passport_list = Passport.query.all()
        cerpac = db.session.query(Cerpac.id).count()
        cerpac_list = Cerpac.query.limit(5).all()
        quota = db.session.query(Quota.id).count()
        quota_list = Quota.query.limit(5).all()
        positions = db.session.query(Lap.id).count()
        position_not_enrolled = db.session.query(Lap).filter(Lap.employee_name == None ).count()
        position_enrolled = db.session.query(Lap).filter(Lap.employee_name != None ).count()
        
        if  position_enrolled == 0:
            percentage = 0
        else:
            percentage = ((position_not_enrolled)/(position_enrolled)) * 100
        
        # Percentage for position available and those not available is calculated below
        # percentage = ((position_not_enrolled)/(position_enrolled)) * 100
        
        position_list=Lap.query.order_by(Lap.timestamp).limit(2).all()
        company_list=Company.query.all()
        companies = db.session.query(Company.id).count()
        emergency = db.session.query(Emergency).count()
        approval = db.session.query(Approve.id).count()
        renew = db.session.query(Renew.id).count()
        folders = db.session.query(Folder.id).count()
        categories = db.session.query(Folder.categories).distinct().all()
        files = db.session.query(File.id).count()

    

    return render_template('home/admin_dashboard.html', title="Dashboard", companies=companies, \
    employee=employee,  passport=passport, cerpac=cerpac, quota=quota, emergency=emergency, \
    positions=positions, approval=approval, renew=renew, folders=folders, files=files,  \
    passport_list=passport_list, company_list=company_list, cerpac_list=cerpac_list, quota_list=quota_list, \
    position_list=position_list, employee_list=employee_list, categories=categories,
    percentage=percentage, position_not_enrolled=position_not_enrolled)



#  website view of the application 
# @bp.route('/') # the home page 
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

@bp.route('/', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home.admin_dashboard'))        
    if request.method == "POST":        
        email = request.form.get('email')
        username = username_from(str(email)) 
        print(email)
        print(username)       
        validate_email = User.query.filter(User.email==email).first()
        if validate_email:
            flash('your email is registered please request for a new password')
            return redirect(url_for('auth.reset_password_request'))
        else:
            user = User(email =email, 
            password = 'default', 
            username=username,
            initiator = 1) 
            db.session.add(user)
            db.session.commit()
            flash('Thank you! please check your email for activation link')
            # send reset password to user    
            send_set_email(user)

            return redirect(url_for('home.signup'))
    return render_template('home/home.html',  title='Sign Up')
    
    
    
    
    return render_template('home/signup.html',
                           title ="Request for Demo")

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