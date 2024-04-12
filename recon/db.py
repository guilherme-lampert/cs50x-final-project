import sqlite3
from flask import current_app, g


# NOTE: This function was inspired by the official Flask documentation. Link: https://flask.palletsprojects.com/en/3.0.x/tutorial/database/
def init_app(app):
    """Ensure that the close_db function will be called after each response to close the connection"""

    app.teardown_appcontext(close_db)


# NOTE: This function was inspired by the official Flask documentation. Link: https://flask.palletsprojects.com/en/3.0.x/tutorial/database/
def get_db():
    """Creates a connection with the database"""

    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


# NOTE: This function was inspired by the official Flask documentation. Link: https://flask.palletsprojects.com/en/3.0.x/tutorial/database/
def close_db(exception):
    """Automatically closes the connection with the database after each response"""

    db = g.pop('db', None)

    if db is not None:
        db.close()