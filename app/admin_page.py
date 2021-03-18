from flask_admin import Admin
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import ModelView
from flask_admin.base import BaseView, expose
from flask_login import current_user
from app.models import User, Dashboard, Role


class MyView(BaseView):
    @expose("/")
    def index(self):
        return self.render("admin_page/index.html")


class SecureModelView(sqla.ModelView):

    form_excluded_columns = ["password"]

    def is_accessible(self):
        # return True
        return current_user.is_authenticated and current_user.role != "admin"


def init_admin(app, db):
    admin = Admin(
        app,
        name="Visual Approach Analytics",
        template_mode="bootstrap3",
    )
    # admin.add_views(SecureModelView(User, db.session))
    admin.add_views(ModelView(User, db.session))
    admin.add_views(ModelView(Role, db.session))
    admin.add_views(ModelView(Dashboard, db.session))
    return admin
