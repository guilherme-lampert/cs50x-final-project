from flask import Blueprint, render_template, flash, jsonify, request, make_response
from recon.db import get_db
from recon.utils import load_countries, load_indicators, load_categories, get_api_data, get_df, login_required

bp = Blueprint("query", __name__, url_prefix="/query")


@bp.route("/")
def index():
    """Loads the refined query menu"""

    return render_template("query/index.html", countries=load_countries(), indicators=load_indicators(), categories=load_categories())


@bp.route("/country-summary")
def country_summary():
    """Loads the result page for a country"""
    
    return render_template("query/country-summary.html")


@bp.route("/refined-query-result")
def refined_query_result():
    """Loads the result page for a specific query"""

    error = None

    if not (requested_countries := request.args.get("country")):
        error = "At least one country must be selected"
    
    elif not (requested_indicators := request.args.get("indicator")):
        error = "At least one indicator must be selected"

    elif not (requested_start_year := request.args.get("start_year")):
        error = "The start year must be informed"

    elif not (requested_end_year := request.args.get("end_year")):
        error = "The end year must be informed"

    elif not requested_start_year.isdigit() or not requested_end_year.isdigit():
        error = "The years must be digits"

    if not error:
        
        try:
            start_year = int(requested_start_year)
            end_year = int(requested_end_year)

            if end_year < start_year:
                error = "The end year can't come before the start year"

            countries = requested_countries.split(",")
            indicators = requested_indicators.split(",")

            if len(countries) > 5:
                error = "Can't select more than 5 countries"

        except Exception as e:
            print("Could not convert the years or lists", e)
            error = "Invalid format for the years"
    
    if not error:
        
        data = get_api_data(countries, indicators, start_year, end_year)
        
        if not data:
            return render_template("query/refined-query-not-result.html")

        return render_template("query/refined-query-result.html", data=data)

    else:
        flash(error)
        return render_template("query/index.html", countries=load_countries(), indicators=load_indicators(), categories=load_categories(), error=error)


@bp.route("/index-search-query-country")
def index_search_query_country():
    """Handles the autocomplete index menu"""

    db = get_db()

    if not (country_request := request.args.get("c")):
        countries = {}

    elif not (submitting_form := request.args.get("s")):
        countries = {}
    
    elif submitting_form == "true":
        countries = db.execute(
            "SELECT * FROM country WHERE name = ?", (country_request,)
        ).fetchone()
        
        if not countries:
            countries = {}
        
        else:
            countries = dict(countries)

    elif submitting_form == "false":
        
        if len(country_request) <= 2:
            countries = db.execute(
                "SELECT * FROM country WHERE name LIKE ?", (country_request + "%",)
            ).fetchall()
            countries = [dict(country) for country in countries]
        
        else:
            countries = db.execute(
                "SELECT * FROM country WHERE name LIKE ?", ("%" + country_request + "%",)
            ).fetchall()
            countries = [dict(country) for country in countries]
    
    else:
        countries = {}
    
    return jsonify(countries)


@login_required
@bp.route("/download", methods=["POST"])
def download():
    """Handles download requests"""
    
    try:
        data = request.json
        df = get_df(data)
    
    except Exception as e:
        print(f"Could not load the data in download view: {e}")
        return None

    # Lines above were made with the help of stack overflow
    # Link: https://stackoverflow.com/questions/38634862/use-flask-to-convert-a-pandas-dataframe-to-csv-and-serve-a-download
    resp = make_response(df.to_csv(index=False))
    resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
    resp.headers["Content-Type"] = "text/csv"
    
    return resp


@login_required
@bp.route("/save-query", methods=["POST"])
def save_query():
    ...