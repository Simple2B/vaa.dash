from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import current_user, login_user, logout_user, login_required

from app.models import User
from app.forms import LoginForm, RegistrationForm, RequestResetForm, ResetPasswordForm
from app.controllers import generate_password_reset_url, send_email, confirm_token
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
        )
        user.set_password(form.password.data)
        user.save()
        # login_user(user)
        flash("Registration successful.", "success")
        log(log.DEBUG, "Registration successful.")

        # SEND CONFIRMATION EMAIL
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            confirm_url = generate_password_reset_url(user.email)
            html = render_template(
                "auth/email_signup_confirmation.html",
                confirm_url=confirm_url,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
            )
            subject = "Greetings from Visual Approach Analytics!"
            send_email(user.email, subject, html)
            log(
                log.DEBUG,
                "A confirmation email has been sent.",
            )

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
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Wrong email or password.", "danger")
            log(log.ERROR, "Wrong email or password.")
            return redirect(url_for("auth.signin"))
        user.authenticated = True
        user.save()
        login_user(user)
        # flash("Login successful.", "success")
        log(log.DEBUG, "Login successful.")
        return redirect(url_for("main.dashboard"))
    return render_template("auth/login.html", form=form)


@auth_blueprint.route("/logout")
@login_required
def logout():
    user = current_user
    user.authenticated = False
    user.save()
    logout_user()
    log(log.DEBUG, "You were logged out.")
    # flash("You were logged out.", "info")
    return redirect(url_for("main.index"))


@auth_blueprint.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    form = RequestResetForm()
    if form.validate_on_submit():
        logout_user()
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            confirm_url = generate_password_reset_url(user.email)
            html = render_template(
                "auth/email_password_reset_confirmation.html",
                confirm_url=confirm_url,
                first_name=user.first_name,
                last_name=user.last_name,
            )
            subject = "Reset password request"
            send_email(user.email, subject, html)
            flash(
                "An email has been sent with instructions to reset your password.",
                "info",
            )
            log(
                log.DEBUG,
                "An email has been sent with instructions to reset your password.",
            )
    return render_template(
        "auth/reset_password_request.html", title="Reset Password", form=form
    )


@auth_blueprint.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    email = "unknown"
    try:
        email = confirm_token(token)
    except Exception:
        flash("The confirmation link is invalid or has expired.", "danger")
        log(log.ERROR, "The confirmation link is invalid or has expired.")
    user = User.query.filter_by(email=email).first_or_404()
    if not user:
        flash("That is an invalid or expired token.", "warning")
        log(log.ERROR, "That is an invalid or expired token.")
        return redirect(url_for("auth.signin"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        user.save()
        flash("Your password has been changed!", "info")
        log(log.DEBUG, "Your password has been changed!")
        return redirect(url_for("auth.signin"))
    return render_template("auth/reset_token.html", form=form)
