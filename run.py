#!/usr/bin/env python
import os
from dotenv import load_dotenv
import time
# import schedule
import click
from datetime import datetime
from config import Config
from app import create_app, db
# from app.check import get_applicant_info, get_cerpac_details, get_status_details,\
    # search_by_cerpac, search_by_form
from app.models import User, Employee, Passport
from app.report import send_report, send_Birthday_messages, send_marketing_mails, \
    send_work_anniversary_messages

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

#  Initialise the app configuration
app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Employee=Employee, Passport=Passport)


@app.cli.command()
def deploy():
    send_report()
    time.sleep(2)
    send_Birthday_messages()
    time.sleep(2)
    send_marketing_mails()
    time.sleep(2)
    send_work_anniversary_messages()

@app.cli.command()
def report():
    """ Run a monthly statutory report for Foldate App"""
    print('Feeding .......')
    users = User.query.all()
    employees = Passport.query.all()
    print('here...',  str(users))
    print('here...',  str(employees))

@app.cli.command()
def scheduled():
    """Run scheduled job."""
    print(str(datetime.utcnow()), 'Importing feeds...')
    send_Birthday_messages()
    print(str(datetime.utcnow()), 'This cron runs every 30 minutes')
    time.sleep(5)
    print(str(datetime.utcnow()), 'Done!')

@app.cli.command()
def birthday():
    send_Birthday_messages()
    print(str(datetime.utcnow()), 'Birthday Messages sent...')

    

