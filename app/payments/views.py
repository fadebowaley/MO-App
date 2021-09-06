import os
import json
import string
import random
import pdfkit
from flask import abort, flash, redirect, render_template, \
url_for, g, jsonify, current_app, request, make_response
from flask_login import current_user, login_required
from wtforms import ValidationError
from datetime import datetime, date
from datetime import date, timedelta
from werkzeug.utils import secure_filename
from sqlalchemy import func
from app.payments import bp
from app import db, session, sessionmaker
from app.models import Chamber, User, Invoice, Tax, Detail, Account, Employee, Company, Payment
from app.payments.forms import InvoiceForm
from wtforms.ext.sqlalchemy.fields import QuerySelectField




def invoiceRef():
    chars = string.digits
    reference ='INV-' + ''.join(random.choice(chars) for _ in range(4))  
    return(reference)


#  we define all the routes that we need for settings
   

    
@bp.route('/invoice/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_invoice(id):
    """
    
    
    """
    
    
    return render_template('payments/receipt-view.html',
                            title="Receipt")
    

    
    
@bp.route('/invoice-settings', methods=['GET', 'POST'])
@login_required
def invoice_settings():
           
    return render_template('settings/invoice-settings.html',
                            title="Invoice Settings")
    
    
@bp.route('/taxes-settings', methods=['GET', 'POST'])
@login_required
def taxes_settings():
       
    
    return render_template('payments/taxes.html',
                            title="Taxes and Deductions")
    

           
