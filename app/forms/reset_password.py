from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, EqualTo


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords do not match."),
        ],
    )
    submit = SubmitField("Submit")

    def validate_password(self, field):
        pass_len = len(field.data)
        if pass_len:
            if pass_len < 6 or pass_len > 30:
                raise ValidationError("Field must be between 6 and 30 characters long.")
