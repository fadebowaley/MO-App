from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMIN)(f)

def account_required(f):
    return permission_required(Permission.ACCOUNT)(f)

def manager_required(f):
    return permission_required(Permission.MANAGE)(f)

def super_required(f):
    return permission_required(Permission.SUPER_ROLE)(f)