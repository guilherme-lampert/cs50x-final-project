from flask import Blueprint

bp = Blueprint('query', __name__)


@bp.route('/')
def index():
    return "hello, world"