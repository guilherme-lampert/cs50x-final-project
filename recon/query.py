from flask import Blueprint, render_template, current_app
from recon.db import get_db

bp = Blueprint("query", __name__, url_prefix="/query")


@bp.route("/")
def index():
    """"""
    return render_template("query/index.html")


@bp.route("/country-summary")
def country_summary():
    """"""
    return render_template("query/country-summary.html")


@bp.route("/refined-query-result")
def refined_query_result():
    """"""
    return render_template("query/refined-query-result.html")