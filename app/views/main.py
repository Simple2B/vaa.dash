from flask import render_template, Blueprint
from flask_login import login_required

from app.models import Dashboard

main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def index():
    dashboards = Dashboard.query.all()
    return render_template("index.html", dashboards=dashboards)


@main_blueprint.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")
