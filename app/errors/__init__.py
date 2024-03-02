from flask import Blueprint

bp = Blueprint(name="error", import_name=__name__)

from app.errors import handlers
