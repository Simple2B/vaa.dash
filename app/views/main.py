from flask import render_template, Blueprint
from flask_login import login_required


main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def index():
    return render_template("index.html")


@main_blueprint.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")
