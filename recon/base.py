from flask import Blueprint, render_template, current_app, request, jsonify, url_for
from recon.db import get_db

bp = Blueprint("base", __name__)


@bp.route("/")
def index():
    """Loads the index page"""

    return render_template("base/index.html")


@bp.route("/tutorial")
def tutorial():
    """Loads the tutorial page"""
    
    return render_template("base/tutorial.html")
