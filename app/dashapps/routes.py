from flask import render_template

from app.dashapps import bp
from app.dashapps.dash_analysis import app as the_first_dash_app_obj
from app.dashapps.dash_yield_curve import app as the_second_dash_app_obj
from app.dashapps.dash_oil_and_gas import app as the_third_dash_app_obj
from app.controllers import verify_role_dash, accessed_links


@bp.route("/the_first_dash_app")
@verify_role_dash
def the_first_dash_app():
    return render_template(
        "dashapps/dash_app.html",
        dash_url=the_first_dash_app_obj.URL_BASE,
        min_height=the_first_dash_app_obj.MIN_HEIGHT,
        dashboards=accessed_links(),
    )


@bp.route("/the_second_dash_app")
@verify_role_dash
def the_second_dash_app():
    return render_template(
        "dashapps/dash_app.html",
        dash_url=the_second_dash_app_obj.URL_BASE,
        min_height=the_second_dash_app_obj.MIN_HEIGHT,
        dashboards=accessed_links(),
    )


@bp.route("/the_third_dash_app")
@verify_role_dash
def the_third_dash_app():
    return render_template(
        "dashapps/dash_app.html",
        dash_url=the_third_dash_app_obj.URL_BASE,
        min_height=the_third_dash_app_obj.MIN_HEIGHT,
        dashboards=accessed_links(),
    )
