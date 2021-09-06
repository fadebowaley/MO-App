from flask import Blueprint

bp = Blueprint('payments', __name__, template_folder='templates', static_folder='static' )


from app.payments import views
