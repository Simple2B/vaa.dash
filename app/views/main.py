from flask import render_template, Blueprint
from app.controllers import accessed_links


main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def index():
    return render_template("index.html", dashboards=accessed_links())
