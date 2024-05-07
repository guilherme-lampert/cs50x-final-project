from flask import Blueprint, flash, redirect, render_template, url_for, request, session, g

from recon.utils import login_required
from recon.db import get_db

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/queries", methods=["GET", "POST"])
@login_required
def queries():

    if request.method == "POST":
        ...
    
    else:

        db = get_db()

        rows = db.execute(
            "SELECT q.id AS query_id, q.name AS query_name, q.start_year AS start_year, q.end_year AS end_year, q.date AS date, "
            "c.name AS country_name, i.category AS indicator_category, i.label AS indicator_label, i.unit AS indicator_unit "
            
            "FROM query AS q "

            "JOIN query_country AS qc "
            "ON q.id = qc.query_id "

            "JOIN query_indicator AS qi "
            "ON q.id = qi.query_id " 

            "JOIN country AS c "
            "ON qc.country_id = c.id "

            "JOIN indicator AS i "
            "ON qi.indicator_id = i.id "

            "WHERE q.user_id = ?",
            (g.user["id"],)
        ).fetchall()

        queries = {}

        for row in rows:

            id = row["query_id"]
            indicator = (row["indicator_category"], row["indicator_label"], row["indicator_unit"])
            
            if id not in queries:
                queries[id] = {
                    "name": row["query_name"],
                    "countries": [row["country_name"]],
                    "indicators": [indicator],
                    "start_year": row["start_year"],
                    "end_year": row["end_year"],
                    "date": row["date"]
                }
            
            else:
                if row["country_name"] not in queries[id]["countries"]:
                    queries[id]["countries"].append(row["country_name"])
                
                if indicator not in queries[id]["indicators"]:
                    queries[id]["indicators"].append(indicator)
                
        return render_template("user/queries.html", queries=queries)


@bp.route("/account", methods=["GET", "POST"])
@login_required
def account():

    if request.method == "POST":
        ...
    
    else:

        return render_template("user/account.html")