from flask import Blueprint, flash, redirect, render_template, url_for, request, session, g
from werkzeug.security import check_password_hash, generate_password_hash

from recon.db import get_db
from recon.utils import check_password, logoff_required

"""
NOTE: Most of the routes were built following the pattern of the official Flask documentation. logout() and load_logged_in_user() are almost the same.
Link: https://flask.palletsprojects.com/en/3.0.x/tutorial/views/
"""

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/signup", methods=["GET", "POST"])
@logoff_required
def signup():
    """Register a new user"""

    if request.method == "POST":
        
        error = None
        db = get_db()

        if not (username := request.form.get("username").lower()):
            error = "Username field is empty"
        
        elif not (password := request.form.get("password")) or not (confirmation := request.form.get("confirmation")):
            error = "Password and/or confirmation fields are empty"

        elif password != confirmation:
            error = "Password and confirmation don't match"

        elif not check_password(password):
            error = "Invalid password"
        
        elif db.execute("SELECT * FROM user WHERE username = ?", (username,)).fetchone():
            error = "Username already exists"

        if not error:
            first_name = request.form.get("first_name")
            last_name = request.form.get("last_name")

            db.execute(
                "INSERT INTO user (username, password, first_name, last_name) VALUES (?, ?, ?, ?)",
                (username, generate_password_hash(password), first_name, last_name)
            )
            db.commit()

            flash(f"Registered. Welcome, {first_name if first_name else username}")
            return redirect(url_for("auth.login"))

        else:
            flash(error)
            return render_template("auth/signup.html", error=error)
    
    return render_template("auth/signup.html")


@bp.route("/login", methods=["GET", "POST"])
@logoff_required
def login():
    """Logs a new user in, creating a session"""
    
    if request.method == "POST":
        
        error = None
        db = get_db()

        if not (username := request.form.get("username").lower()):
            error = "Username field is empty"
        
        elif not (password := request.form.get("password")):
            error = "Password field is empty"

        elif not (user := db.execute(
            "SELECT * FROM user WHERE username = ?",
            (username,)).fetchone()):
            error = "Incorrect username"
        
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password"

        if not error:
            session.clear()
            session['user_id'] = user['id']

            flash(f"Welcome, {username}")
            return redirect(url_for('base.index'))
        else:
            flash(error)
            return render_template("auth/login.html", error=error)
    
    return render_template("auth/login.html")


@bp.route('/logout')
def logout():
    """Logs the current user out"""
    
    session.clear()
    
    flash("Logged out")
    return redirect(url_for('base.index'))


@bp.before_app_request
def load_logged_in_user():
    """Checks for a session cookie and loads the user if it exists"""
    
    user_id = session.get("user_id")

    if not user_id:
        g.user = None
    
    else:
        g.user = get_db().execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()
