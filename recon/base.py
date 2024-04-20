from flask import Blueprint, render_template, current_app

bp = Blueprint("base", __name__)


@bp.route("/")
def index():
    """"""

    return render_template("base/index.html")


@bp.route("/tutorial")
def tutorial():
    """"""
    return render_template("base/tutorial.html")