from flask import Blueprint, render_template, current_app, abort, request
from recon.db import get_db

bp = Blueprint("query", __name__, url_prefix="/query")


@bp.route("/")
def index():
    """"""

    db = get_db()

    countries = db.execute(
        "SELECT * FROM country"
    ).fetchall()

    indicators = db.execute(
        "SELECT * FROM indicator"
    ).fetchall()

    categories = ['National accounts', 'People', 'Prices', 'Government finance', 'Balance of payments']

    return render_template("query/index.html", countries=countries, indicators=indicators, categories=categories)


@bp.route("/country-summary")
def country_summary():
    """"""
    return render_template("query/country-summary.html")


@bp.route("/refined-query-result")
def refined_query_result():
    """"""
    return render_template("query/refined-query-result.html")
