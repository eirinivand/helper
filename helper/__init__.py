import os

from flask import Flask, render_template


def create_app():
    # create and configure the app
    happ = Flask(__name__, instance_relative_config=True)
    happ.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY") or 'dev_key',
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

    import helper.db
    db.init_app(happ)
    import helper.auth
    happ.register_blueprint(auth.bp)
    import helper.validate
    happ.register_blueprint(validate.bp)
    happ.add_url_rule('/', endpoint='csvvalidator')

    return happ

