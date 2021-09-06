from flask import render_template, current_app
from app.email import send_email



def send_welcome_email(user):
        send_email(('[Briefkase] Welcome to Expartio'),
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email], 
               text_body=render_template('settings/emails/welcome_email.txt', user=user, ),
               html_body=render_template('settings/emails/welcome_email.html', user=user,))

def send_confirmation_email(user):
        token = user.get_confirmation_token()
        send_email(('[No-reply] Confirm your Account'),
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email], 
               text_body=render_template('settings/emails/confirm.txt', user=user, token=token, external=True),
               html_body=render_template('settings/emails/confirm.html', user=user, token=token, external=True))


def send_reset_email(user):
        token = user.get_reset_token()
        send_email(('[Expat Care] Reset Your Password'),
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('settings/emails/reset_password.txt', user=user, token=token, external=True),
               html_body=render_template('settings/emails/reset_password.html', user=user, token=token, external=True))




        
