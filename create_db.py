import os
from datetime import datetime
from config import Config
from app import create_app, db
from app.models import db, Role, User

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# Telling SQLAlchemy what app should be used as the database model
def create_roles(): 
    permissions = [1, 2, 4, 8, 16]
    perm=0
    for s in range(0, len(permissions)):
        name = ['User', 'Administrator', 'Accountant', 'Manager', 'Super']
        perm=perm + permissions[s]
        name = name[s]
        check = Role.query.filter(Role.name == name).first()
        if check:
            print('user {} already exists.....skip '.format(check.name))
            continue
        set_role = Role( name = name, permissions = perm )
        db.session.add(set_role)
        db.session.commit()
        # Create the first user
        print('User {} created succesfully!'.format(set_role.name))
        if perm == 1:
            print(s+1)
            try:
                user = User(username='User', first_name='John', 
                last_name='Ibukun', email='user@brvcase.com', role_id = s+1)
                db.session.add(user)
                db.session.commit()
                print('added first user')
                # set the User Password
                user.set_password('brvcase')
                db.session.commit()
                print('user created . . . .  ')        
            except:
                print('Error; cannot create Users')
        if perm == 3:
            print(s+1)
            try:
                admin = User(username='Admin', first_name='John', 
                last_name='Doe', email='admin@brvcase.com', role_id = s+1)
                db.session.add(admin)
                db.session.commit()
                print('added first')
                # set the User Password
                admin.set_password('brvcase')
                db.session.commit()
                print('admin created ...')        
            except:
                print('Error; cannot create admin')
        if perm == 7:
            print(s+1)
            try:
                account = User(username='Accountant', first_name='John', 
                last_name='Doe', email='account@brvcase.com', role_id = s+1)
                db.session.add(account)
                db.session.commit()
                print('added first')
                # set the User Password
                account.set_password('brvcase')
                db.session.commit()
                print('super admin created')        
            except:
                print('Error; cannot create account')
        if perm == 15:
            print(s+1)
            try:
                manager = User(username='Manager', first_name='John', 
                last_name='Doe', email='manager@brvcase.com', role_id = s+1)
                db.session.add(manager)
                db.session.commit()
                print('manager user added first')
                # set the User Password
                manager.set_password('brvcase')
                db.session.commit()
                print('super admin created')        
            except:
                print('Error; cannot create Managers')                
        if perm == 31:
            print(s+1)
            try:
                super_user = User(username='SuperAdmin', first_name='John', 
                last_name='Doe', email='super@brvcase.com', role_id = s+1)
                db.session.add(super_user)
                db.session.commit()
                print('added first')
                # set the User Password
                super_user.set_password('brvcase')
                db.session.commit()
                print('super admin created')        
            except:
                print('Error; cannot create Super Users')         
            
    print('Roles configured successfully..')
    
         
 
        
with app.app_context():
    # print('I am here sir') 
    # db.drop_all()   
    db.create_all() # this will create all the tables
    create_roles() #T   his should create all the Roles and Permissions
    print('Configuration set Successfully')
