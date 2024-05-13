import os
from flask import Flask


def create_app():
    """Application factory"""

    app = Flask(__name__)
    
    app.config.from_mapping(
        SECRET_KEY='c1bb9201953ed4c42209d8dc90e9a349582aaf897f35b6ab4afd31153a050069',
        DATABASE=os.path.join(app.root_path, 'recon.db')
    )
    
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import user
    app.register_blueprint(user.bp)

    from . import base
    app.register_blueprint(base.bp)

    from . import query
    app.register_blueprint(query.bp)

    return app