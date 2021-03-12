from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.base import BaseView, expose

from app.models import User


class MyView(BaseView):
    @expose("/")
    def index(self):
        return self.render("admin_page/index.html")


def init_admin(app, db):
    admin = Admin(
        app,
        name="Visual Approach Analytics",
        template_mode="bootstrap3",
        # index_view=CustomAdminIndexView(name="Home", url="/admin"),
    )
    # admin.add_views(SecureModelView(User, db.session))
    admin.add_views(ModelView(User, db.session))
    return admin
