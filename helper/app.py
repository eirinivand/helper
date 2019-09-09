import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

db = None


def create_app():
    global db
    db = SQLAlchemy()

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY") or 'dev_key',
        SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL"),
    )
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def home():
        return render_template("home.html")

    db.init_app(app)
    from helper import auth
    app.register_blueprint(auth.bp)
    from helper import validate
    app.register_blueprint(validate.bp)
    app.add_url_rule('/', endpoint='csvvalidator')

    return app
