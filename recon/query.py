from flask import Blueprint, render_template, flash, jsonify, request, g, make_response
from recon.db import get_db
from recon.utils import load_countries, load_indicators, load_categories, get_api_data, get_df, login_required
import datetime

bp = Blueprint("query", __name__, url_prefix="/query")


@bp.route("/")
def index():
    """Loads the refined query menu"""

    return render_template("query/index.html", countries=load_countries(), indicators=load_indicators(), categories=load_categories())


@bp.route("/country-summary")
def country_summary():
    """Loads the result page for a country"""

    error = ""

    db = get_db()
    
    if not (country := request.args.get("country")) or country == "none":
        error = "The country was not selected"

    elif not db.execute(
        "SELECT * FROM country WHERE acronym = ?", (country,)
    ).fetchone():
        error = "Invalid parameter for country"
    
    if not error:

        country = [country]

        db_indicators = load_indicators()
        indicators = []

        for indicator in db_indicators:
            
            if indicator["category"] == "National accounts" and indicator["acronym"] in ["NGDP_RPCH", "NGDPDPC"]:
                indicators.append(indicator["acronym"])
            
            elif indicator["category"] != "National accounts":
                indicators.append(indicator["acronym"])

        end_year = datetime.datetime.now().year
        start_year = end_year - 9

        data = get_api_data(country, indicators, start_year, end_year)

        if not data:
            return render_template("query/no-result.html")

        if g.user:
            save_param = {
                'countries': country,
                'indicators': indicators,
                'start_year': start_year,
                'end_year': end_year
            }
        
        else:
            save_param = None
        
        return render_template("query/result.html", data=data, save_param=save_param)

    else:
        flash(error)
        return render_template("base/index.html", countries=load_countries(), indicators=load_indicators(), categories=load_categories(), error=error)


@bp.route("/result")
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
            print("Could not convert the years or lists: ", e)
            error = "Invalid format for the parameters"
    
    if not error:
        
        data = get_api_data(countries, indicators, start_year, end_year)
        
        if not data:
            return render_template("query/no-result.html")
        
        if g.user:
            save_param = {
                'countries': countries,
                'indicators': indicators,
                'start_year': start_year,
                'end_year': end_year
            }
        
        else:
            save_param = None

        return render_template("query/result.html", data=data, save_param=save_param)

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
    """Handles save query requests"""

    status = ""
    db = get_db()

    try:
        data = request.json

        if not (name := data.get("name")):
            status = "Missing name. The query was not saved."
        
        elif not (start_year := data.get("start_year")):
            status = "Missing start year. The query was not saved."
        
        elif not (end_year := data.get("end_year")):
            status = "Missing end year. The query was not saved."

        elif not (countries := data.get("countries")):
            status = "Missing countries. The query was not saved."

        elif not (indicators := data.get("indicators")):
            status = "Missing indicators. The query was not saved."

        elif not isinstance(countries, list):
            status = "Incorrect type for countries. The query was not saved."
        
        elif not isinstance(indicators, list):
            status = "Incorrect type for indicators. The query was not saved."

        elif len(db.execute("SELECT * FROM query WHERE user_id = ?", (g.user["id"],)).fetchall()) >= 10:
            status = "You can't save more than 10 queries."
    
    except Exception as e:
        print(f"Could not load the data in save query view: {e}")
        status = "An error occoured, the query was not saved."

    if not status:
    
        try:
            query_id = db.execute(
                "SELECT * FROM query WHERE name = ? AND user_id = ?", (name, g.user["id"],)
            ).fetchone()

            if not query_id:
                
                current_date = datetime.datetime.now().strftime("%m-%d-%Y %H:%M")

                db.execute(
                    "INSERT INTO query (name, start_year, end_year, date, user_id) VALUES (?, ?, ?, ?, ?)",
                    (name, start_year, end_year, current_date, g.user["id"])
                )

                query_id = db.execute(
                    "SELECT * FROM query WHERE name = ? AND user_id = ?", (name, g.user["id"],)
                ).fetchone()["id"]

                for country in countries:
                    
                    country_id = db.execute(
                        "SELECT * FROM country WHERE acronym = ?", (country,)
                    ).fetchone()["id"]
                    
                    db.execute(
                        "INSERT INTO query_country (query_id, country_id) VALUES (?, ?)",
                        (query_id, country_id)
                    )
                
                for indicator in indicators:

                    indicator_id = db.execute(
                        "SELECT * FROM indicator WHERE acronym = ?", (indicator,)
                    ).fetchone()["id"]

                    db.execute(
                        "INSERT INTO query_indicator (query_id, indicator_id) VALUES (?, ?)",
                        (query_id, indicator_id)
                    )

                db.commit()

                status = "Query successfully saved!"
            
            else:
                status = "This query name already exists"
        
        except Exception as e:
            print(f"Could not save the data in query view: {e}")
            status = "An error occoured, the query was not saved."

    return status
