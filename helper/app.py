import os

from flask import Flask, render_template


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY") or 'dev_key',
        DATABASE=os.path.join(app.instance_path, 'helper.sqlite'),
      )
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def home():
        return render_template("home.html")

    from helper.db import init_app
    init_app(app)
    from helper import auth
    app.register_blueprint(auth.bp)
    from helper import validate
    app.register_blueprint(validate.bp)
    app.add_url_rule('/', endpoint='csvvalidator')

    return app
