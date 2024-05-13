from flask import Blueprint, render_template, current_app, request, jsonify, url_for
from recon.db import get_db
from recon.utils import load_categories, load_indicators

bp = Blueprint("base", __name__)


@bp.route("/")
def index():
    """Loads the index page"""

    return render_template("base/index.html")


@bp.route("/tutorial")
def tutorial():
    """Loads the tutorial page"""

    db = get_db()

    categories = load_categories()
    indicators = load_indicators()
    
    return render_template("base/tutorial.html", indicators=indicators, categories=categories)
