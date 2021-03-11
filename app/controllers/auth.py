import pycountry
from itsdangerous import URLSafeTimedSerializer

from flask import current_app, url_for
from flask_mail import Message

from app import mail
from app.logger import log


def country_choices():
    country_name = [country.name for country in pycountry.countries]
    return country_name


def generate_password_reset_url(email):
    """Generates token for password reset"""
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    token = serializer.dumps(email, salt=current_app.config["SECURITY_PASSWORD_SALT"])
    confirm_url = url_for("auth.reset_password", token=token, _external=True)
    return confirm_url


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config["MAIL_DEFAULT_SENDER"],
    )
    try:
        mail.send(msg)
    except ConnectionError as e:
        log(log.ERROR, "Connection error. Turn on your router: %s", e)


def confirm_token(token, expiration=43200):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        email = serializer.loads(
            token, salt=current_app.config["SECURITY_PASSWORD_SALT"], max_age=expiration
        )
    except Exception:
        return False
    return email
