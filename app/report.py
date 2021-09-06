import os
import time
from datetime import datetime, date
from . import db
from flask import current_app, render_template
from .email import send_email, send_bday, send_anny, send_mkt, send_notification_report
from .models import User, Employee, \
Cerpac,  Company, Emergency,  \
Passport, Quota, User, Token_serial, Lap, Renew, \
 Approve, Folder, File





def send_report():
    """ Send Monthly Stutory report to email and copy a folder"""
    print('About to send report ....')
    """
    1. A comprehensive report about company quota on a table spread
    2. The report should be sent to report Folder with a name and date
    3. Folder is created and a new File is created in the Folder named Monthly Report
    4. An alert Message is sent to the admin email concerning this report and a link
    5. The report should have csv version and pdf.
    """
    print(str(datetime.utcnow()), 'Importing feeds...')
    users=User.query.all()
    for user in users:
        print('|| userid {},|| email:{}, || username:{}'.format(user.id, user.email, user.username))
        print(str(datetime.utcnow()), 'Done!')
    time.sleep(5)
    print(str(datetime.utcnow()), 'Done!')
    
""" 1. Check if the application has the client birthday for today
    2. get the client name, email and date
    3. Trigger a customised report to the client wishing him a fulfilling Birthday
    4. Send also a cusomised sms - using Twillio for Birthday message
"""
def send_Birthday_messages():
    bday = Employee.query.filter(Employee.get_bday != "").all()
    for employee in bday:
        chk = employee.get_bday[1]
        if chk == 0:
            # print(employee.id, employee.email, employee.first_name, employee.last_name, employee.get_bday[0])
            print('Happy Birthday to you {} , {} !'.format(employee.first_name, employee.get_bday[0]))         
            recipient = employee.email
            send_bday(('[Moments] Happy Birthday to you'),
            sender=current_app.config['ADMINS'][0],
            recipients=[recipient],
            text_body=render_template('email/birthday.txt', employee=employee),
            html_body=render_template('email/birthday.html', employee=employee))
            print('email has been  sent!')
            print('Done !')


def send_work_anniversary_messages():
    anniversary = Employee.query.filter(Employee.get_anny != "").all()
    for employee in anniversary:
        chk = employee.get_anny[1]
        if chk == 0:
            print('Happy Work Anniversary to you {} , {} !'.format(employee.first_name, employee.get_bday[0]))         
            recipient = employee.email
            send_bday(('[Moments] Happy work anniversary to you'),
            sender=current_app.config['ADMINS'][0],
            recipients=[recipient],
            text_body=render_template('email/anniversary.txt', employee=employee),
            html_body=render_template('email/anniversary.html', employee=employee))
            print('Work Anniversary email has been  sent!')
            print('Done!')
        



def send_marketing_mails():
    " Send periodic emails for customer Acquisition"
    """
    1. Create an email marketing for target customers and get it running
    2. make acqusition easy by helping tham to manage their clients
    """
    print(str(datetime.utcnow()), 'Marketing effort')
    time.sleep(3)
    print(str(datetime.utcnow()), 'sent Marketing maetrials')
    time.sleep(2)
    pass




