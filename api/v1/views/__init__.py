"""app_views Blueprint API"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


from v1.views.user.user import *
from v1.views.staff.staff import *
from v1.views.admin.admin import *