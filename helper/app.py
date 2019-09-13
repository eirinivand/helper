import os

from helper import db

from helper import auth
from helper import validate
from flask import Flask, render_template

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


db.init_app(app)

app.register_blueprint(auth.bp)

app.register_blueprint(validate.bp)
app.add_url_rule('/', endpoint='csvvalidator')
