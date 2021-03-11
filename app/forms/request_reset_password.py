from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    ValidationError,
)
from wtforms.validators import DataRequired, Email
from app.models import User


class RequestResetForm(FlaskForm):
    email = StringField(
        "Email Address",
        validators=[DataRequired(), Email(message="Enter a valid email.")],
    )
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("There is no account with that email.")
