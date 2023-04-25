from flask import Blueprint

bp = Blueprint('qa', __name__, url_prefix='/')
@bp.route('/')
def login():
    pass