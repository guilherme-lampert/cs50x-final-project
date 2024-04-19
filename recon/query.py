from flask import Blueprint, render_template
from recon.db import get_db

bp = Blueprint("query", __name__)


@bp.route("/")
def index():
    """"""
    return render_template("query/index.html")


@bp.route("/tutorial")
def tutorial():
    """"""
    return render_template("query/tutorial.html")