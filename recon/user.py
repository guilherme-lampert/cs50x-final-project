from flask import Blueprint, flash, redirect, render_template, url_for, request, session, g
from werkzeug.security import check_password_hash, generate_password_hash

from recon.utils import login_required, load_user_queries, check_password
from recon.db import get_db

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/account")
@login_required
def account():
    """Loads the account page"""

    db = get_db()

    error = request.args.get('error')

    user = db.execute(
        "SELECT * FROM user WHERE id = ?", (g.user["id"],)
    ).fetchone()

    return render_template("user/account.html", user=user, error=error)


@bp.route("/change-username", methods=["POST"])
@login_required
def change_username():
    """Changes the username"""

    db = get_db()
    error = ""
    
    if not (username := request.form.get("username")):
        error = "Missing username"
    
    elif not (password := request.form.get("password")):
        error = "Missing password"
    
    elif not check_password_hash(g.user["password"], password):
        error = "Incorrect password."
    
    elif db.execute("SELECT * FROM user WHERE username = ?", (username,)).fetchone():
        error = "Username already exists"

    if not error:
        
        db.execute(
            "UPDATE user SET username = ? "
            "WHERE id = ?", (username, g.user["id"],)
        )
        db.commit()
        flash("Username changed")
    
    else:
        flash(error)
        params = {"error": error}
        return redirect(url_for('user.account', **params))
    
    return redirect(url_for('user.account'))


@bp.route("/change-password", methods=["POST"])
@login_required
def change_password():
    """Changes the user password"""

    error = ""

    if not (current_password := request.form.get("current_password")):
        error = "Missing the current password"
    
    elif not (new_password := request.form.get("new_password")):
        error = "Missing the new password"

    elif not (confirm_password := request.form.get("confirm_password")):
        error = "Missing the confirmation password"
    
    elif new_password != confirm_password:
        error = "Password and confirmation don't match"
    
    elif not check_password(new_password):
        error = "Invalid new password"

    elif not check_password_hash(g.user["password"], current_password):
        error = "Incorrect current password"
    
    if not error:
        
        db = get_db()

        db.execute(
            "UPDATE user SET password = ? "
            "WHERE id = ?", (generate_password_hash(new_password), g.user["id"],)
        )
        db.commit()
        flash("Password updated")

    else:
        flash(error)
        params = {"error": error}
        return redirect(url_for('user.account', **params))
        
    return redirect(url_for('user.account'))


@bp.route("/change-full-name", methods=["POST"])
@login_required
def change_full_name():
    """Changes the first name and/or last name"""

    db = get_db()

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")

    db.execute(
        "UPDATE user SET first_name = ?, last_name = ? "
        "WHERE id = ?", (first_name, last_name, g.user["id"],)
    )
    db.commit()

    flash("Named changed")
    return redirect(url_for('user.account'))


@bp.route("/delete-account", methods=["POST"])
@login_required
def delete_account():
    """Deletes the user account"""

    error = ""

    if not (password := request.form.get("password")):
        error = "Missing the current password"

    elif not (confirm_password := request.form.get("confirm_password")):
        error = "Missing the confirmation password"

    elif password != confirm_password:
        error = "Password and confirmation don't match"

    elif not check_password_hash(g.user["password"], password):
        error = "Incorrect current password"

    if not error:
        
        db = get_db()

        # deletar usuario e queries desse usuario

        user_queries = db.execute(
            "SELECT * FROM query WHERE user_id = ?", (g.user["id"],)
        ).fetchall()
        user_queries = [query["id"] for query in user_queries]

        for id in user_queries:
            db.execute(
                "DELETE FROM query_country WHERE query_id = ?", (id,)
            )

            db.execute(
                "DELETE FROM query_indicator WHERE query_id = ?", (id,)
            )

            db.execute(
                "DELETE FROM query WHERE id = ?", (id,)
            )
        
        db.execute(
            "DELETE FROM user WHERE id = ?", (g.user["id"],)
        )
        
        db.commit()

        session.clear()
        flash("Account deleted")
        return redirect(url_for('base.index'))
    
    else:
        flash(error)
        params = {"error": error}
        return redirect(url_for('user.account', **params))


@bp.route("/queries", methods=["GET", "POST"])
@login_required
def queries():
    """If get, loads the user queries. If post, redirects to the search query view"""

    if request.method == "POST":

        error = ''
        db = get_db()
        
        if not (id := request.form.get('id')):
            error = 'Missing id'
        
        elif not (db.execute(
            "SELECT * FROM query WHERE id = ? AND user_id = ?", (id, g.user["id"],)
        )).fetchone():
            error = 'This query does not exist.'

        if error:
            flash(error)
            queries = load_user_queries(g.user["id"])
            return render_template("user/queries.html", queries=queries)
        
        else:

            row = db.execute(
                "SELECT * FROM query WHERE id = ?", (id,)
            ).fetchone()
            start_year = row["start_year"]
            end_year = row["end_year"]

            rows = db.execute(
                "SELECT c.acronym AS country_acronym "
                
                "FROM country AS c "
                
                "JOIN query_country AS qc "
                "ON c.id = qc.country_id "
                
                "JOIN query AS q "
                "ON q.id = qc.query_id "
                
                "WHERE q.id = ?", (id,)
            
            ).fetchall()
            countries = [row["country_acronym"] for row in rows]
            countries = ",".join(countries)
            
            rows = db.execute(
                "SELECT i.acronym AS indicator_acronym "

                "FROM indicator AS i "

                "JOIN query_indicator AS qi "
                "ON i.id = qi.indicator_id "

                "JOIN query AS q "
                "ON q.id = qi.query_id "

                "WHERE q.id = ?", (id,)
            ).fetchall()
            indicators = [row["indicator_acronym"] for row in rows]
            indicators = ",".join(indicators)

            params = {
                "country": countries,
                "indicator": indicators,
                "start_year": start_year,
                "end_year": end_year
            }
            
            return redirect(url_for('query.refined_query_result', **params))
    
    else:
        queries = load_user_queries(g.user["id"])
        return render_template("user/queries.html", queries=queries)


@bp.route("/delete-query", methods=["POST"])
@login_required
def delete_query():
    """Delets the query from the database"""

    error = ''
    db = get_db()

    if not (id := request.form.get('id')):
        error = 'Missing id'

    elif not (db.execute(
        "SELECT * FROM query WHERE id = ? AND user_id = ?", (id, g.user["id"],)
    )).fetchone():
        error = 'This query does not exist'

    if error:
        flash(error)
    
    else:
        db.execute(
            "DELETE FROM query_country WHERE query_id = ?", (id,)
        )

        db.execute(
            "DELETE FROM query_indicator WHERE query_id = ?", (id,)
        )

        db.execute(
            "DELETE FROM query WHERE id = ?", (id,)
        )

        db.commit()
        
    return redirect(url_for('user.queries'))
