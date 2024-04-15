import os
from flask import Flask


def create_app():
    """Application factory"""

    app = Flask(__name__)
    
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.root_path, 'recon.db'),
    )
    
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import query
    app.register_blueprint(query.bp)

    from . import stock_mkt
    app.register_blueprint(stock_mkt.bp)

    return app