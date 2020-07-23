from flask import Blueprint

main = Blueprint('main', __name__)

from app.main import views, models, errors, wg_api
