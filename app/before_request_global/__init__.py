from flask import Blueprint

before_request_global = Blueprint('before_request_global', __name__)

from . import g_global
