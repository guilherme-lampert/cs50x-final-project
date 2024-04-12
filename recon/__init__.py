from flask import Flask


def create_app():
    """Application factory"""

    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    from . import authorization
    app.register_blueprint(authorization.bp)

    from . import query
    app.register_blueprint(query.bp)

    from . import stock_mkt
    app.register_blueprint(stock_mkt.bp)

    return app