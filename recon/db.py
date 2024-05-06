import sqlite3
from flask import current_app, g

"""
NOTE: Most of the functions here were built following the pattern of the official Flask documentation. init_app and close_db are almost the same.
Link: https://flask.palletsprojects.com/en/3.0.x/tutorial/database/
"""


def init_app(app):
    """Ensures that the close_db function will be called after each response to close the connection"""
    
    app.teardown_appcontext(close_db)


def get_db():
    """Creates a connection with the database"""

    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(exception):
    """Closes the connection with the database"""

    db = g.pop('db', None)

    if db is not None:
        db.close()
