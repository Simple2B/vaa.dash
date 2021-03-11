from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    ValidationError,
    SelectField,
)
from wtforms.validators import DataRequired, Email, Length, EqualTo

from app.models import User
from app.controllers import country_choices


class RegistrationForm(FlaskForm):
    first_name = StringField("First name", validators=[DataRequired(), Length(1, 30)])
    last_name = StringField("Last name", validators=[DataRequired(), Length(1, 30)])
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    country = SelectField(
        "Country",
        validators=[DataRequired()],
        choices=[c for c in country_choices()],
        coerce=str,
    )
    organization = StringField("Organization")
    password = PasswordField("Password", validators=[DataRequired(), Length(6, 30)])
    password_confirmation = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords do not match."),
        ],
    )
    submit = SubmitField("Sign up")

    def validate_email(form, field):
        if User.query.filter_by(email=field.data).first() is not None:
            raise ValidationError("This email is already registered.")

    def validate_password(self, field):
        pass_len = len(field.data)
        if pass_len:
            if pass_len < 6 or pass_len > 30:
                raise ValidationError("Field must be between 6 and 30 characters long.")
