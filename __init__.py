import os

from flask import Flask, render_template


def create_app():
    # create and configure the app
    happ = Flask(__name__, instance_relative_config=True)
    happ.config.from_mapping(
        DATABASE=os.path.join(happ.instance_path, 'helper.sqlite'),
    )
    # ensure the instance folder exists
    try:
        os.makedirs(happ.instance_path)
    except OSError:
        pass

    @happ.route("/")
    def home():
        return render_template("home.html")

    import db
    db.init_app(happ)
    import auth
    happ.register_blueprint(auth.bp)
    import validate
    happ.register_blueprint(validate.bp)
    happ.add_url_rule('/', endpoint='csvvalidator')

    return happ
