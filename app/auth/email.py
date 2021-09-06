from flask import render_template, current_app
from email.utils import formataddr
#from flask_babel import _
from flask import *  
from flask_mail import *  
from app.email import send_email
from flask_login import login_required, login_user,\
     logout_user, current_user



def send_welcome_email(user):
        send_email((f'{user.first_name} We are Excited as you are'),
                sender = formataddr(('Congratulations - Brvcase Team', current_app.config['ADMINS'][0] )), 
               recipients=[user.email], 
               text_body=render_template('email/welcome_email.txt', user=user, ),
               html_body=render_template('email/welcome_email.html', user=user,))
        
        

def send_confirmation_email(user):
        token = user.get_confirmation_token()
        send_email(('[No-reply] Confirm your Account'),
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email], 
               text_body=render_template('email/confirm.txt', user=user, token=token, external=True),
               html_body=render_template('email/confirm.html', user=user, token=token, external=True))
        


def send_reset_email(user):
        token = user.get_reset_token()
        send_email((f'{user.username} password reset from brvcase'),
               sender = formataddr(('Brvcase password Reset', current_app.config['ADMINS'][0] )), 
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt', user=user, token=token,  external=True),
               html_body=render_template('email/reset_password.html', user=user, token=token, external=True))
        
def send_set_email(user):
        token = user.get_reset_token()
        send_email(('hello {}, -  Welcome to brvcase ! '.format(user.username)),
               sender = formataddr(('Brvcase Start Your Journey!', current_app.config['ADMINS'][0] )), 
        #        sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/set_password.txt', user=user, current_user=current_user, token=token, external=True),
               html_body=render_template('email/set_password.html', user=user, current_user=current_user, token=token, external=True),                   )
        



def send_invite_email(user):
        token = user.get_reset_token()
        send_email(('Invitation to join {}  from {} {} '.format(current_user.chamber.company,  current_user.first_name, current_user.last_name  )),
               sender = formataddr(('Brvcase - Invitation Card', current_app.config['ADMINS'][0] )), 
               recipients=[user.email],
               text_body=render_template('email/send_invite.txt', user=user, current_user=current_user, token=token, external=True),
               html_body=render_template('email/send_invite.html', user=user, current_user=current_user, token=token, external=True))




        
