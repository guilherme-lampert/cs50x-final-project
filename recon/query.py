from flask import Blueprint
from recon.db import get_db

bp = Blueprint('query', __name__)


@bp.route('/')
def index():
    db = get_db()

    user = db.execute("SELECT * FROM user").fetchall()
    print(user[0]["username"])
    return f"hello, {user[0]['username']}"