
import os
import string
import random
import emoji
import pathlib
from app.settings  import bp
from app import db, session, sessionmaker
from app.models import User
from flask import abort, flash, redirect, render_template, \
url_for, g, jsonify, current_app, request
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from pathlib import Path
from PIL import Image
from ..decorators import admin_required, permission_required, account_required,\
    manager_required, super_required
from app.settings.forms import VendorForm, RegistrationForm, UpdateAccountForm, VendorModuleForm
from .email import  send_welcome_email, send_reset_email, send_confirmation_email

# @bp.app_context_processor
# def inject_permissions():
#     return dict(Permission=Permission)

ALLOWED_EXTENSIONS = set(['.jpg', '.png', '.gif', '.pdf', '.csv', '.doc','docx', '.xls', '.xlsx','.txt' ])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def Accountid():
    chars = string.digits
    # serial ='EMP-ID 000' + ''.join(random.choice(chars) for _ in range(4))
    accountid ='2104' + ''.join(random.choice(chars) for _ in range(4))
    new_accountid=int(accountid)
    return(new_accountid)
    


#  We list here all Clients that has been setup
@bp.route('/vendor/view', methods=['GET', 'POST'])
@login_required
@super_required
def list_vendors():
    if not current_user.role.permissions ==31:
        
        vendors = Vendor.query.filter_by(id =current_user.vendor_id).all()
    else:
        vendors = Vendor.query.all()      
    return render_template('settings/vendor/vendors.html',
                           vendors=vendors, title="Customers Lists" )
    
    
    
@bp.route('/vendor/add', methods=['GET', 'POST'])
@login_required
@super_required
def company_settings():
    # We create a vendor that house the operations this will be assigned to users
    company_settings=True
    form = VendorForm()
    if form.validate_on_submit():           
        if request.method == 'POST':       
            vendor = Vendor(
            company_address=str(form.company_address.data).upper(),
            company=str(form.company.data).upper(),
            company_email=str(form.company_email.data).upper(), 
            phone_number=str(form.phone_number.data).upper(),
            city = str(form.city.data).upper(),
            state = str(form.state.data).upper(),
            country = str(form.country.data).upper(),
            postal_code =str(form.postal_code.data).upper(),
            accountid = Accountid(),
            contact_person = (form.contact_person.data).upper(),
            contact_phone = (form.contact_phone.data).upper(),
            website = (form.website.data).upper()
            )
            logo_file = request.files['logo_file']
            if logo_file and request.form.get('logo_file') !="":                
                #if logo_image and allowed_file(logo_image.filename) and form.company_name.data != "" and form.company_email.data != "":
                filename = secure_filename(logo_file.filename)
                logo_file.save(os.path.join(current_app.root_path,'static/logos', filename))
                vendor.logo_file=filename                         
            try:        
                db.session.add(vendor)
                db.session.commit()
                # Send a Welcome Message to thee Contact Email
                flash('You have successfully added {}' .format(vendor.company) )
            except:
            
                flash('Error: vendor name already exists.')
        
        return redirect(url_for('settings.list_vendors'))
          
    return render_template('settings/vendor/vendor.html',
                            title="Company Settings", form=form)
    
    
@bp.route('/vendor/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@super_required
def edit_company_settings(id):
    company_settings = False
    vendor = Vendor.query.get_or_404(id)
    form = VendorForm(obj=vendor)
    if form.validate_on_submit():     
        
        vendor.company=form.company.data
        vendor.company_address=form.company_address.data 
        vendor.company_email=form.company_email.data
        vendor.phone_number=form.phone_number.data
        vendor.city=form.city.data
        vendor.state=form.state.data
        vendor.country=form.country.data
        vendor.postal_code=form.postal_code.data
        vendor.contact_person=form.contact_person.data
        vendor.contact_phone=form.contact_phone.data
        vendor.website=form.website.data
        if request.method == 'POST':            
                db.session.commit()
                flash('You have successfully edited {}' .format(vendor.company))
        
        return redirect(url_for('settings.list_vendors'))
        form.company_name.data = company.company_name
        form.company_address.data = company.company_address
        form.company_email.data = company.company_email
        form.contact_number.data = company.contact_number

    return render_template('settings/vendor/vendor.html', action="Edit",
                            form=form,
                           company_settings=company_settings, vendor=vendor, title="Edit Company")


@bp.route('/vendor/delete/<int:id>', methods=['GET', 'POST'])
@login_required
@super_required
def delete_company_settings(id):
    """   Delete an company settings  from the company database """
    vendor = Vendor.query.get_or_404(id)
    check = User.query.filter_by(vendor_id=id).all()
    if check:
        flash('Company cannot be closed ! Please delete Users first')
        return redirect(url_for('settings.list_vendors'))
    db.session.delete(vendor)
    db.session.commit()
    flash('You have successfully deleted {}' .format(vendor.company))
    return redirect(url_for('settings.list_vendors'))
    return render_template(title="Delete vendor")
    
    
# we create users and assigns them to different companies so that they can use the account separately
    
@bp.route('/vendor/activations/<int:id>',  methods=['GET', 'POST'])
@login_required
@super_required
def modules_roles_settings(id):
    vendor = Vendor.query.get_or_404(id)
    users = User.query.filter(User.vendor_id==id).all()

    if request.method == 'POST':
        # Below form activate immigration module
        if request.form['submit_button'] == 'i-active':                        
            if vendor.is_immigration != 1:
                vendor.is_immigration = 1
                flash('immigration module activated !')
            else:
                vendor.is_immigration = 0
                flash('immigration deactivated !')
            db.session.commit() 
            
            # This form will activate realestate module  
        elif request.form['submit_button'] == 'r-active':            
            if vendor.is_realestate != 1:
                vendor.is_realestate = 1
                flash('realestate module activated !')
            else:
                vendor.is_realestate = 0
                flash('realestate deactivated !')
            db.session.commit()   
        # This form will activate entertainment module  
        elif request.form['submit_button'] == 'e-active':            
            if vendor.is_entertainment != 1:
                vendor.is_entertainment = 1
                flash('entertainment module activated !')
            else:
                vendor.is_entertainment = 0
                flash('entertainment deactivated !')
            db.session.commit()
         
        # This form will activate intellectual property    
        elif request.form['submit_button'] == 'I-active':            
            if vendor.is_Iproperty != 1:
                vendor.is_Iproperty = 1
                flash('entertainment module activated !')
            else:
                vendor.is_Iproperty = 0
                flash('entertainment deactivated !')
            db.session.commit()        

        # This form will activate Self Services        
        elif request.form['submit_button'] == 'S-active':            
            if vendor.is_services != 1:
                vendor.is_services = 1
                flash('self-service module activated !')
            else:
                vendor.is_services = 0
                flash('self-service deactivated !')
            db.session.commit()   

        # This form will activate Billings and Payment        
        elif request.form['submit_button'] == 'b-active':            
            if vendor.is_Billings != 1:
                vendor.is_Billings = 1
                flash('Billings module activated !')
            else:
                vendor.is_Billings = 0
                flash('Billings deactivated !')
            db.session.commit()  
             
        # This form will activate Billings and Payment        
        elif request.form['submit_button'] == 'p-active':            
            if vendor.is_probate != 1:
                vendor.is_probate = 1
                flash('Probate module activated !')
            else:
                vendor.is_probate = 0
                flash('Probate deactivated !')
            db.session.commit()

    return render_template('settings/roles/roles-permission.html',                           
       vendor=vendor, users=users, title="Module and Roles Activations" )
    



@bp.route('/users', methods=['GET', 'POST'])
@login_required
@super_required
def list_users():
    users = User.query.all() 

    return render_template('settings/users/users.html',
                           users=users, title="users")
               

@bp.route('/users/register', methods=['GET', 'POST'])
@login_required
@super_required
def create_user():
    """  Add a user to the database    """    
    form = RegistrationForm()
    if form.validate_on_submit():                        
        user = User(username =form.username.data.lower(),
        first_name=form.first_name.data,
        last_name=form.last_name.data,
        email=form.email.data,
        password=form.password.data,
        role = form.role.data,
        vendor = form.vendor.data)
        db.session.add(user)
        db.session.commit()        
        token = user.get_confirmation_token()
        print(token)
        flash('You have successfully added a new user.')

        return redirect(url_for('settings.list_users'))
    # load user template
    return render_template('settings/users/user.html', action="Add",
                            form=form,
                           title="Create User")
    



@bp.route('/users/create/<int:id>', methods=['GET', 'POST'])
@login_required
@super_required
def add_user(id):
    """  Add a user to the database    """
    form = RegistrationForm()
    # Get the Vendor id first
    vendor = Vendor.query.get_or_404(id)
    if request.method =='POST':                
        user = User(
        username = form.username.data,
        email=form.email.data,
        password = 'default',
        first_name = form.first_name.data,
        last_name =form.last_name.data,
        role_id = 4, #default to admin role 5
        vendor_id = vendor.id
        )
        db.session.add(user)
        db.session.commit()
        flash("user created successfully")

    # # load user template
    return redirect(url_for('settings.modules_roles_settings', id=vendor.id))


@bp.route('/users/role/<int:id>', methods=['GET', 'POST'])
@login_required
@super_required
def change_role(id):
    """  Add a user to the database    """
    user = User.query.get_or_404(id)
    flash("user = {} vendor = {}".format(user.id, user.vendor.id))
    return redirect(url_for('settings.modules_roles_settings', id=current_user.vendor.id))
 
    




#  this function is for activations 
@bp.route('/users/activate/<int:id>', methods=['GET', 'POST'])
@login_required
@super_required
def activate_user(id):
    user = User.query.get_or_404(id)
    print(user.id)
    if user:        
        if user.confirmed != True:
            # activate_user(user)
            user.confirmed = True
            flash('User activated !')
        else:
            user.confirmed = False
            flash('User deactivated !') 
        db.session.commit()
        return redirect(url_for('settings.list_users'))
    return redirect(url_for('settings.list_users'))

# set the vendor to null for super user to work on tables:

       
#  this functions is for edit users
@bp.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@super_required
def edit_user(id):   
    user = User.query.get_or_404(id)
    form = RegistrationForm(obj=user)

    if request.method =='POST':
               
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.role = form.role.data
        user.vendor =  form.vendor.data

        # db.session.add(user)        
        db.session.commit()
        flash('You have successfully edited the user.')
        # redirect to the users page
        return redirect(url_for('settings.list_users'))
    
    form.first_name.data = user.first_name
    form.last_name.data = user.last_name
    form.vendor.data = user.vendor   
    return render_template('settings/users/user_edit.html', action="Edit",
                         form=form,
                           user=user, title="Edit User")

#  This is a functions for deleting users 
@bp.route('/users/delete/<int:id>', methods=['GET', 'POST'])
@login_required
@super_required
def delete_user(id):
    # - UnboundLocalError
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('You have successfully deleted the user.')
    # redirect to the users page
    return redirect(url_for('settings.list_users'))
    return render_template(title="Delete User")



@bp.route('/users/show/<int:id>')
@login_required
@super_required
def show_user(id):
    #users = User.query.all()
    user = User.query.get_or_404(id)
    if user.id == id:
            found_user = user
    return render_template('settings/users/show.html', 
                           user = found_user, 
                           show_user=show_user, 
                           title="Show User" )
    
    
    
@bp.route('/users/permissions/<int:id>')
@login_required
def role_user(id):
    # get the user id
    user =User.query.get_or_404(id)
    # set user as ADMIN ROLE
    role = Role.query.filter(name == 'Administrator').first()
    # update the user id
    user.role_id = role.id
    print(user.id)
    print(role.id)

    return redirect(url_for('modules_roles_settings', id=user.vendor.id))   
    
    
  

#  we define all the routes that we need for settings
@bp.route('/brand', methods=['GET', 'POST'])
@login_required
def brand():
        
    return render_template('settings/brand.html',
                            title="settings")
    
    
@bp.route('/password', methods=['GET', 'POST'])
@login_required
def change_password():
        
    return render_template('settings/change-password.html',
                            title="Change Password")
    
    

    
    
@bp.route('/localization', methods=['GET', 'POST'])
@login_required
def localization():
        
    return render_template('settings/locals.html',
                            title="localization")
    
@bp.route('/roles-permission', methods=['GET', 'POST'])
@login_required
def role_permissions():
        
    return render_template('settings/roles-permission.html',
                            title="Permission")
    
    
@bp.route('/lock', methods=['GET', 'POST'])
@login_required
def role_lock():
           
    return render_template('settings/lock-screen.html',
                            title="Lock")
    
    
@bp.route('/invoice-settings', methods=['GET', 'POST'])
@login_required
def invoice_settings():
           
    return render_template('settings/invoice-settings.html',
                            title="Invoice Settings")
    
    
@bp.route('/notifications', methods=['GET', 'POST'])
@login_required
def notification_settings():
           
    return render_template('settings/notifications.html',
                            title="Invoice Settings")
    
    
@bp.route('/taxes', methods=['GET', 'POST'])
@login_required
def taxes_settings():
           
    return render_template('settings/taxes.html',
                            title="Taxes and Deductions Settings")
    
@bp.route('/roles', methods=['GET', 'POST'])
@login_required
def roles_settings():
           
    return render_template('settings/roles/roles_settings.html',
                            title="User Roles & Priviledges")