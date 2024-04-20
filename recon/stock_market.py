from flask import Blueprint, render_template

bp = Blueprint('stock_market', __name__, url_prefix="/stock-market")


@bp.route("/")
def index():
    """"""
    return render_template("stock_market/index.html")