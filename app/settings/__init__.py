from flask import Blueprint

bp = Blueprint('settings', __name__, template_folder='templates', static_folder='static' )


from app.settings import views
