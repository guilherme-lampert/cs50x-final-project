from flask import redirect, g, url_for
from werkzeug.exceptions import abort
from recon.db import get_db
import re
import functools
import requests
import pandas as pd


def check_password(password):
    """Check if user password is valid when registering or changing"""

    regex = "^(?=.*?[0-9])(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^a-zA-Z0-9_]).{8,}$"

    if re.search(regex, password):
        return True

    return False


def login_required(view):
    """Checks if the user is logged in"""

    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        
        if not g.user:
            abort(401)

        return view(*args, **kwargs)

    return wrapped_view


def logoff_required(view):
    """Checks if a user is not logged in"""

    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        
        if g.user:
            return redirect(url_for('base.index'))

        return view(*args, **kwargs)

    return wrapped_view


def load_countries():
    """Load the countries from the database"""

    db = get_db()

    countries = db.execute(
        "SELECT * FROM country"
    ).fetchall()

    return countries


def load_indicators():
    """Load the indicators from the database"""

    db = get_db()

    indicators = db.execute(
        "SELECT * FROM indicator"
    ).fetchall()

    return indicators


def load_categories():
    """Load the categories from the database"""

    # The categories are hard coded because i want them to show in this exact order, so getting it from the db and then changing the order for this would just be worse.
    return ['National accounts', 'People', 'Prices', 'Government finance', 'Balance of payments']


def get_api_data(countries, indicators, start_year, end_year):
    """Gets the API data and modifies it, adding extra information"""

    # This function was made with the help of Chat GPT. The idea was mine, but the AI helped me with some of the logic and some syntax that i did not know 

    base_url = "https://www.imf.org/external/datamapper/api/v1/"

    url = base_url + "/".join(indicators) + "/" + "/".join(countries)
    url = url + "?periods=" + ",".join([str(year) for year in range(start_year, end_year + 1)])
    
    try:
        api_data = requests.get(url).json()

        if "values" not in api_data:
            return None
        
        api_data = api_data["values"]
        db = get_db()

        categories = load_categories()
        data = {}

        for indicator, countries in api_data.items():
            for country, years in countries.items():
                db_row = db.execute(
                    "SELECT * FROM country WHERE acronym = ?", (country,)
                ).fetchone()

                countries[country] = {
                    'name': db_row["name"],
                    'years': years
                }
            
            db_row = db.execute(
                "SELECT * FROM indicator WHERE acronym = ?", (indicator,)
            ).fetchone()
            
            api_data[indicator] = {
                'countries': countries,
                'info': {
                    'label': db_row["label"],
                    'unit': db_row["unit"]
                }
            }

        for category in categories:
            for indicator in api_data:
                db_row = db.execute(
                    "SELECT * FROM indicator WHERE acronym = ?", (indicator,)
                ).fetchone()

                if category == db_row["category"]:
                    if category not in data:
                        data[category] = {indicator: api_data[indicator]}
                    
                    else:
                        data[category].update({indicator: api_data[indicator]})
            
            if category in data:
                for indicator in data[category]:
                    api_data.pop(indicator)
        
        return data

    except Exception as e:
        print("Erro ao fazer a solicitação para o IMF API ou BD: ", e)
        return None


def get_df(data):
    """Builds a dataframe from pandas with the data returned by the get_api_data() function"""

    columns = ['category', 'indicator', 'unit', 'country', 'year', 'value']
    df = pd.DataFrame(columns=columns)

    try:
        for category, indicators in data.items():

            row_category = category
            
            for indicator, indicator_values in indicators.items():

                row_indicator = indicator_values['info']['label']
                row_unit = indicator_values['info']['unit']
                
                for country, country_values in indicator_values['countries'].items():

                    row_country = country_values['name']
                    
                    for year, year_value in country_values['years'].items():
                        
                        row_year = year
                        row_value = year_value

                        new_row = pd.Series({
                            'category': row_category,
                            'indicator': row_indicator,
                            'unit': row_unit,
                            'country': row_country,
                            'year': row_year,
                            'value': row_value
                        })
                        
                        df = pd.concat([df, new_row.to_frame().T], ignore_index=True)
        
        return df
    
    except Exception as e:
        print(f"An error occoured during the get_df() utils function: {e}")
        return None
    

def load_user_queries(user_id):
    """Loads all the queries of that user"""
    
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
        (user_id,)
    ).fetchall()

    queries = {}

    for row in rows:

        id = row["query_id"]

        indicator_category = row["indicator_category"]
        indicator_values = (row["indicator_label"], row["indicator_unit"])
        
        if id not in queries:
            queries[id] = {
                "name": row["query_name"],
                "countries": [row["country_name"]],
                "indicators": {indicator_category: [indicator_values]},
                "start_year": row["start_year"],
                "end_year": row["end_year"],
                "date": row["date"]
            }

        else:
            if row["country_name"] not in queries[id]["countries"]:
                queries[id]["countries"].append(row["country_name"])
            
            if indicator_category not in queries[id]["indicators"]:
                queries[id]["indicators"].update({indicator_category: [indicator_values]})
            
            elif indicator_category in queries[id]["indicators"] and indicator_values not in queries[id]["indicators"][indicator_category]:
                queries[id]["indicators"][indicator_category].append(indicator_values)
    
    return queries