from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import current_user, login_user, logout_user, login_required

from app.models import User
from app.forms import LoginForm, RegistrationForm
from app.logger import log

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            country=form.country.data,
            organization=form.organization.data,
            password=form.password.data,
        )
        user.save()
        # login_user(user)
        flash("Registration successful.", "success")
        log(log.DEBUG, "Registration successful.")
        return redirect(url_for("auth.signin"))
    elif form.is_submitted():
        for error in form.errors:
            for msg in form.errors[error]:
                log(log.ERROR, "signup(): %s", msg)
                flash(msg, "danger")
    return render_template("auth/register.html", form=form)


@auth_blueprint.route("/signin", methods=["GET", "POST"])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.authenticate(form.email.data, form.password.data)
        if user is not None:
            login_user(user)
            # flash("Login successful.", "success")
            log(log.DEBUG, "Login successful.")
            return redirect(url_for("main.dashboard"))
        flash("Wrong email or password.", "danger")
        log(log.ERROR, "Wrong email or password.")
    return render_template("auth/login.html", form=form)


@auth_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    # flash("You were logged out.", "info")
    return redirect(url_for("main.index"))
