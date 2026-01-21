from flask import Blueprint

index_bp = Blueprint('index_bp', __name__, url_prefix='/')


@index_bp.route('/')
def index():
    return {"Status": "OK"}
