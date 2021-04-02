from flask import (
    render_template,
    flash,
    Response,
    redirect,
)
from flask_admin import Admin
from flask_admin.contrib import sqla
from flask_admin.base import expose, AdminIndexView

# from flask_security import current_user
from werkzeug.exceptions import HTTPException


from app import basic_auth
from app.models import User, Dashboard, Role
from app.controllers import send_email, generate_password_reset_url
from app.logger import log


class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(
            message,
            Response(
                "You could not be authenticated. Please refresh the page.",
                401,
                {"WWW-Authenticate": 'Basic realm="Login Required"'},
            ),
        )


class MyView(AdminIndexView):
    @expose("/")
    def index(self):
        return self.render("admin_page/index.html")


class UserModelView(sqla.ModelView):
    create_template = "admin_page/create_user.html"

    form_excluded_columns = ("password_hash", "signup_at", "authenticated")
    column_exclude_list = ["password_hash"]
    column_searchable_list = ["email"]
    column_filters = [
        "first_name",
        "last_name",
        "email",
        "country",
        "organization",
        "authenticated",
        "signup_at",
        "role",
    ]

    # def is_accessible(self):
    #     return current_user.role != "admin"

    def is_accessible(self):
        if not basic_auth.authenticate():
            log(log.WARNING, "Not authenticated.")
            raise AuthException("Not authenticated.")
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())

    def after_model_change(self, form, model, is_created):
        if is_created:
            confirm_url = generate_password_reset_url(model.email)
            html = render_template(
                "auth/email_signup_confirmation_from_admin_page.html",
                confirm_url=confirm_url,
                first_name=model.first_name,
                last_name=model.last_name,
                email=model.email,
            )
            subject = "Greetings from Visual Approach Analytics!"
            send_email(
                model.email,
                subject,
                html,
            )
            flash(
                f"An email has been sent for user {model.first_name} {model.last_name} to the address {model.email} for setting the account with a password.",
                "info",
            )
            log(
                log.DEBUG,
                "A confirmation email has been sent.",
            )


class RoleModelView(sqla.ModelView):
    column_searchable_list = ["name"]
    column_filters = ["name", "dashboard"]

    # def is_accessible(self):
    #     return current_user.role != "admin"

    def is_accessible(self):
        if not basic_auth.authenticate():
            log(log.WARNING, "Not authenticated.")
            raise AuthException("Not authenticated.")
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())


class DashboardModelView(sqla.ModelView):
    column_searchable_list = ["title"]
    column_filters = [
        "title",
        "url",
        "available_to_unregistered_user",
        "available_to_registered_user",
        "role",
    ]

    # def is_accessible(self):
    #     return current_user.role != "admin"

    def is_accessible(self):
        if not basic_auth.authenticate():
            log(log.WARNING, "Not authenticated.")
            raise AuthException("Not authenticated.")
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())


def init_admin(app, db):
    admin = Admin(
        app,
        template_mode="bootstrap3",
    )
    admin.add_views(UserModelView(User, db.session))
    admin.add_views(RoleModelView(Role, db.session))
    admin.add_views(DashboardModelView(Dashboard, db.session))
    return admin
