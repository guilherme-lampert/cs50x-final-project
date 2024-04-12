from flask import Flask


def create_app():
    """Application factory"""

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')


    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'Hello, World!'

    return app