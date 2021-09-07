import os
import string
from PIL import Image
import base64
import io
import time
import pyotp
import qrcode
import emoji
import random
from flask import current_app
from app import db
from app.auth import bp
import datetime
from datetime import datetime, date
from flask import Flask, session, render_template, redirect, url_for, \
     flash, request, abort, send_from_directory
from flask_login import login_required, login_user,\
     logout_user, current_user
from .email import send_email
from app.auth.forms import LoginForm, ResetPasswordRequestForm, ResetPasswordForm, \
    RegistrationForm, VendorForm
from werkzeug.utils import secure_filename
from app.models import User
from app.auth.email import  send_welcome_email, send_reset_email, \
    send_confirmation_email , send_set_email, send_invite_email
import secrets
from PIL import Image




ALLOWED_EXTENSIONS = set(['.jpg', '.png', '.gif', '.pdf', '.csv', '.doc','docx', '.xls', '.xlsx','.txt' ])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def Accountid():
    chars = string.digits
    # serial ='EMP-ID 000' + ''.join(random.choice(chars) for _ in range(4))
    accountid ='2104' + ''.join(random.choice(chars) for _ in range(4))
    new_accountid=int(accountid)
    return(new_accountid)

@bp.before_app_request
def before_request():
    try:
        if current_user.is_authenticated and current_user.confirmed:
            if current_user.vendor_id == None or current_user.role_id == None:
                # if request.blueprint != 'auth' and request.endpoint != 'static':
                return redirect(url_for('auth.onboarding'))
    except:        
        return redirect(url_for('home.admin_dashboard'))                 
       



"""function to resize pictures"""
def save_logo(logo):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(logo.filename)
    picture_fn_logo = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/logos', picture_fn_logo)
    output_size = (125, 125)
    i = Image.open(logo)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn_logo

def save_picture(picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profiles', picture_fn)
    output_size = (125, 125)
    i = Image.open(picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


# This is a way to set up a new company for a new user, we enforce the route
@bp.route('/onboarding')
def onboarding():
    if current_user.vendor_id != None or current_user.role_id != None:                
        return redirect(url_for('home.homepage'))
    return render_template('auth/onboarding.html')


        
        
@bp.route('/signup', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home.admin_dashboard'))
    form = RegistrationForm()
    # if form.validate_on_submit() and request.method == 'POST':
    if request.method == "POST":
        email = form.email.data
        username = form.username.data
        validate_email = User.query.filter(User.email==email).first()
        validate_username = User.query.filter(User.username==username).first()
        if validate_email:
            flash('your email is registered please request for a new password')
            return redirect(url_for('auth.reset_password_request'))
        elif validate_username:
            flash('your  username is taken, please use another username')
            return render_template('auth/signup.html', form=form, title='Sign Up')
        else:
            user = User(email =form.email.data, 
            password = 'default', 
            username=form.username.data,
            initiator = 1) 
            db.session.add(user)
            db.session.commit()
            flash('Thank you! please check your email for activation link')
            # send reset password to user    
            send_set_email(user)
            return redirect(url_for('auth.login'))
    return render_template('auth/signup.html', form=form, title='Sign Up')





@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
    # if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(
                form.password.data):
                if form.password.data == 'default':
                    send_reset_email(user)
                    flash('Please check your email for activation link')                  
                    return redirect(url_for('auth.login'))
                else:                                            
                    # log user in
                    login_user(user)
                    session['email'] = form.email.data
                    value = session.get('email')                    
                    #User can signup. if user has no role                    
                    if current_user.vendor_id == None:
                        flash("We are delighted to have you onboard !, Quickly do a 2 minutes setup \
                            for your company so that you can have a \
                              wonderful clients experience")
                        return redirect(url_for('auth.welcome'))
                        # return redirect(url_for('auth.onboarding'))          
                    return redirect(url_for('home.admin_dashboard'))
        else:
            flash('Password link expires after 5 minutes, request a new link')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')






@bp.route('/welcome', methods=['GET', 'POST'])
# @login_required
def  welcome():
    # We create a vendor that house the operations this will be assigned to users
    form = VendorForm()       
    if request.method == 'POST':        
        company = form.company.data
        company_email  = form.company_email.data
        contact_phone = form.contact_phone.data
        contact_person = form.contact_person.data
        company_address = form.company_address.data
        city = form.city.data
        state = form.state.data
        country = form.country.data
        website = form.website.data
        industry = request.form.get('industry')       
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        gender = request.form.get('gender')
        birthday = request.form.get('birthday')
        role_id = request.form['role']
        postal_code = request.form.get('postal_code')
        logo_file = request.files['logo_file']        
        if logo_file and request.form.get('logo_file') !="":
            save_logo_file = save_logo(logo_file)
                
        vendor = Vendor( 
            logo_file = save_logo_file,
            company=str(company).upper(),
            company_email=str(form.company_email.data).upper(), 
            contact_phone = str(form.contact_phone.data).upper(),
            contact_person = str(form.contact_person.data).upper(),
            company_address=str(form.company_address.data).upper(),
            industry = str(industry).upper(),            
            city = str(form.city.data).upper(),
            state = str(form.state.data).upper(),
            country = str(form.country.data).upper(),
            website = (form.website.data).upper(),
            postal_code =str(form.postal_code.data).upper(),            
            accountid = Accountid(),
            )
        #Add to database  
        try:
            db.session.add(vendor)
            db.session.commit()
            # db.session.no_autoflush()
            print('New company account is created')
        except:
            print('Error: cannot new company account')                                            
        image_file = request.files['image_file']
        if image_file and request.form.get('image_file') !="":
            save_picture_profile = save_picture(image_file)          
        current_user.image_file = save_picture_profile
        current_user.role_id = role_id
        current_user.vendor_id = vendor.id
        current_user.first_name = first_name
        current_user.last_name = last_name
        current_user.birthday = birthday
        current_user.gender = gender
        current_user.accountid = vendor.accountid
        current_user.initiator = 1
                # update user tables 
        try:
            db.session.commit()
            flash('Please scan the Barcode and activate your account')
            print('user sucessfully updated')
        except:
            flash('User Updating, Please try again')
            return render_template('auth/onboarding.html',
                            title="Onboarding", form=form)
            flash('Please scan the Barcode and activate your account')
                # return redirect
        return redirect(url_for('auth.welcome_2fa')) 
                # send a one time code to email for confirmation
        return redirect(url_for('auth.account'))
    return render_template('auth/onboarding.html',
                            title="Onboarding", form=form)



# 2FA page route
@bp.route("/welcome/otp/")
def welcome_2fa():    
    user = User.query.filter(User.id == current_user.id).first()
    # print(user.email)
    email = user.email        
    # generating random secret key for authentication                   
    base32secret = pyotp.random_base32()
    # generating q_code for authentication
    totp_uri = pyotp.totp.TOTP(base32secret).provisioning_uri(
    email, issuer_name="Brvcase.com")
    img = qrcode.make(totp_uri)
    img.save('qr_code.png')
    im = Image.open("qr_code.png")
    data = io.BytesIO()
    im.save(data, "PNG")
    encoded_img_data = base64.b64encode(data.getvalue())        

    return render_template("auth/otp_factor.html", secret=base32secret,  img_data=encoded_img_data.decode('utf-8'))



# 2FA form route
@bp.route("/welcome/otp/", methods=["POST"])
def welcome_2fa_form():    
    secret = request.form.get("secret")
    print(secret)
    otp = int(request.form.get("otp"))
    print(otp)
    # verifying submitted OTP with PyOTP
    if pyotp.TOTP(secret).verify(otp):
        flash("Your 2FA token is valid and successful!", "success")
        user=User.query.filter(User.username==current_user.username).first()
        if user:
            user.active = True
            db.session.commit()
        # return to dashboard or profile
        return redirect(url_for("auth.account"))
    else:
        # inform users if OTP is invalid
        flash("You have supplied an invalid 2FA token!", "danger")
        return redirect(url_for("auth.welcome_2fa"))
    


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully been logged out.')
    # redirect to the login page
    return redirect(url_for('home.homepage'))


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('home.admin_dashboard'))
    form = ResetPasswordRequestForm()
    if request.method =="POST":
    # if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:            
            #send_password_reset_email(user)
            send_reset_email(user)
            flash('Check your email for the instructions to reset your password')
        return redirect(url_for('auth.login'))
    return render_template('auth/password_request.html',
                           title='Reset Password', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home.admin_dashboard'))
    user = User.verify_reset_token(token)
    if not user:
        flash('invalid or expired token', 'warning')
        return redirect(url_for('auth.login'))  
    form = ResetPasswordForm()
    if request.method =="POST":
    # if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/password_reset.html', form=form, title= "Reset password")


# After registration this link will help user to reset their password 
@bp.route('/set_password/<token>', methods=['GET', 'POST'])
def set_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home.admin_dashboard'))
    user = User.verify_reset_token(token)
    if not user:
        flash('invalid or expired token', 'warning')
        return redirect(url_for('auth.login'))  
    form = ResetPasswordForm()
    if request.method =="POST":
    # if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Password Updated! Welcome!!.')        
        login_user(user)
        email = user.email
        print(email)
        session['email'] = email
        value = session.get('email')
        if current_user.vendor_id == None:
                                               
            return redirect(url_for('auth.welcome'))
        
        if current_user.invitee == 1:
            return redirect(url_for('auth.invitation'))        
      
        return redirect(url_for('home.admin_dashboard'))              
      
     
    return render_template('auth/set_password2.html', form=form, title= "Start with a password")




@bp.route('/invitation/', methods=['GET', 'POST'])
@login_required
def invitation():       
    form = RegistrationForm()
    if request.method =="POST":        
        image_file = request.files['image_file']
        filename = secure_filename(image_file.filename)        
        if image_file and request.form.get('image_file') !="":
            try:
                filename = save_picture(image_file) 
            except:
                flash('cannot add passport')
        current_user.username = request.form.get('username')
        current_user.first_name = request.form.get('first_name')
        current_user.last_name = request.form.get('last_name')
        current_user.gender= request.form.get('gender')
        current_user.birthday = request.form.get('birthday')
        current_user.invitee = 1
        current_user.image_file = filename
        #  update user tables with below
        db.session.commit()      
        return redirect(url_for('home.homepage'))           

    return render_template('auth/invite.html', form=form, title= "Set your profile", current_user=current_user)



    


@bp.route("/account", methods=['GET', 'POST'])
@login_required
def account():
      
    if request.method == 'GET':
        if current_user.is_authenticated:
            user=User.query.filter_by(username=current_user.username) 
            
            invitee= User.query.filter(User.vendor_id == current_user.vendor_id
            ).filter(User.invitee != 0).all()          
        return render_template('auth/profile.html', title='Account', current_user=current_user,
                               vendor = current_user.vendor, invitee=invitee)
     






@bp.route("/account/Billings", methods=["POST", 'GET'])
def Billings():    
    vendor = Vendor.query.filter(Vendor.id==current_user.vendor_id).first()  
    if current_user.initiator == 1:
            
        if  not vendor.is_Billings == 1:
                    
            vendor.is_Billings = 1
            db.session.commit()       
            flash('Billings module activated !')
        
        else:
            vendor.is_Billings = 0             
            db.session.commit()           
            flash('Billings module deactivated !')
        
    else:
        flash('Please contact Gneneral Admin for settings')    
    return redirect(url_for('auth.account'))


@bp.route("/account/immigrations", methods=["POST", 'GET'])
def immigrations():
    
    vendor = Vendor.query.filter(Vendor.id==current_user.vendor_id).first()      
    if current_user.initiator == 1:
        
        if  not vendor.is_immigration == 1:        
            vendor.is_immigration = 1
            db.session.commit()       
            flash('immigration module activated !')
        
        else:
            vendor.is_immigration = 0             
            db.session.commit()           
            flash('immigration module deactivated !')
    else:
        flash('Please contact Admin to enable immigration module') 
    return redirect(url_for('auth.account'))


@bp.route("/account/probates", methods=["POST", 'GET'])
def probates():    
    vendor = Vendor.query.filter(Vendor.id==current_user.vendor_id).first()      
    if  not vendor.is_probate == 1:        
        vendor.is_probate = 1
        db.session.commit()       
        flash('probate module activated !')
        
    else:
        vendor.is_probate = 0             
        db.session.commit()           
        flash('probate module deactivated !')
    return redirect(url_for('auth.account'))


@bp.route("/account/realestates", methods=["POST", 'GET'])
def realestates():
    
    vendor = Vendor.query.filter(Vendor.id==current_user.vendor_id).first()      
    if  not vendor.is_realestate == 1:        
        vendor.is_realestate = 1
        db.session.commit()       
        flash('realestate module activated !')
        
    else:
        vendor.is_realestate = 0             
        db.session.commit()           
        flash('realestate module deactivated !')
    return redirect(url_for('auth.account'))

  
""" change emails requires otp """  

@bp.route('/account/edit/', methods=['GET', 'POST'])
@login_required
def edit_user():
    if current_user.is_authenticated:
        """ Edit an account  """
        form = UpdateAccountForm()
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                current_user.image_file = picture_file
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.company = form.company.data
            current_user.gender = form.gender.data
            current_user.company_address = form.company_address.data
            current_user.city = form.city.data
            current_user.phone_number = form.phone_number.data
            #current_user.state = form.state.data
            #current_user.date_of_birth = form.date_of_birth.data
            db.session.commit()
            flash('You have successfully edited your profile.')

            # redirect to the roles page
            return redirect(url_for('auth.account'))
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.first_name.data  =  current_user.first_name
        form.last_name.data =  current_user.last_name
        form.company.data =  current_user.company
        form.gender.data =  current_user.gender
        form.company_address.data =  current_user.company_address
        form.city.data =  current_user.city
        form.phone_number.data =  current_user.phone_number
        #form.state.data =  current_user.state
        #form.date_of_birth.data =  current_user.date_of_birth
        image_file = url_for('static', filename='passports/' + current_user.image_file)
        return render_template('auth/edit-profile.html', title='Edit Profile',
                           image_file=image_file, form=form, current_user=current_user)
        
        
        
        
        


""" Creating a Team Member and Inviting them """
@bp.route('/invite/', methods=['GET', 'POST'])
def team_invite():        
    form = RegistrationForm()   
    if request.method == "POST":        
        email = request.form.get('email')
        role = request.form['role']
        name = request.form.get('name')
        print(email, role, name)
        print('we get this one ')        
        validate_email = User.query.filter(User.email==email).first()        
        validate_team = Teamate.query.filter(Teamate.email==email).first()            
       
        if validate_email:
            flash('This Email is registered! user can request for password')
            return redirect(url_for('auth.account'))
        
        if validate_team:
            flash('This Email is has already been sent a request!')
            return redirect(url_for('auth.account'))        
        user = User(email = email, 
                    role_id = role, 
                    username = name,
                    invitee = 1,
        vendor_id = current_user.vendor_id, accountid = current_user.accountid,
        invitee_name = name)
        flash('Activation link sent to your Teamates, please you may need to inform them')
        db.session.add(user)
        # send user by picking the user
        user = User.query.filter(User.email == email).first()
        send_set_email(user)
        user.timesend = datetime.utcnow()
        flash('Email sent!')
        db.session.commit()               
                                             
        return redirect(url_for('auth.account'))
    return render_template('auth/profile.html', form=form, title='Sign Up')

""" Resend the invite again """


@bp.route('/re-invite/<int:id>', methods=['GET', 'POST'])
def team_re_invite(id):            
        # get the user
    if request.method == "GET":
        user = User.query.get_or_404(id)

        if user.role_id:
            check_time = datetime.utcnow()
            print(user.timesend)
            print(check_time)
            # sub = check_time - user.timesend
            # print(sub)
            flash('User has already been invited')
            send_set_email(user)
            return redirect(url_for('auth.account'))
        else:            
            send_set_email(user)
            flash('email has been re-sent  to {}! '.format(user.username))                                   
            return redirect(url_for('auth.account'))
    return redirect(url_for('auth.account'))
   

@bp.route('/email', methods=['GET', 'POST'])
def email_test():
    
    return render_template('email/set_password3.html', user=current_user)



""" view the invitee on the dashboard"""

@bp.route('/account', methods=['GET', 'POST'])
def team_view_invitees():
    
    user= User.query.filter(
    User.vendor_id == current_user.vendor_id
    ).filter(User.invitee == 1).all()

    
    return render_template('auth/profile.html', user=user, title='Sign Up')


@bp.route('/delete/user/<int:id>', methods=['GET', 'POST'])
def delete_user(id):
    
    user = User.query.get_or_404(id)
    # team = Teamate.query.filter(Teamate.email== user.email).first()
    if user:       
        try:
            db.session.delete(user)
            # db.session.delete(team)
            db.session.commit()
            
            flash('user  has been deleted successfully')
            return redirect(url_for('auth.account'))
        except:
            
            flash('User cannot be deleted,. please try again')
    
    return render_template('auth/profile.html', user=user, title='Sign Up')