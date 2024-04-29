from flask import Blueprint, render_template, current_app, request, jsonify
from recon.db import get_db

bp = Blueprint("base", __name__)


@bp.route("/")
def index():
    """"""

    return render_template("base/index.html")


# Inspired by the CS50 Flask class
@bp.route("/search-country")
def search_country():
    """"""

    q = request.args.get("q")
    
    if q:
        db = get_db()
        countries = db.execute(
            "SELECT * FROM country WHERE name LIKE ?", ("%" + q + "%",)
        ).fetchall()
        
        countries = [dict(country) for country in countries]
    
    else:
        countries = []
    
    return jsonify(countries)


@bp.route("/tutorial")
def tutorial():
    """"""
    return render_template("base/tutorial.html")
