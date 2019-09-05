from flask import Flask, render_template


def create_app():
    happ = Flask(__name__)

    @happ.route("/")
    def home():
        return render_template("home.html")

    import validate
    happ.register_blueprint(validate.bp)
    happ.add_url_rule('/', endpoint='csvvalidator')

    return happ


if __name__ == "__main__":
    happ.add_url_rule('/csvvalidator', endpoint='upload_file')
    happ.run(debug=True)
