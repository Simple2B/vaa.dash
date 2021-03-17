from flask_login import current_user
from app.models import Dashboard


def show_accessed_links():
    dashboards = []
    for dash in Dashboard.query.all():
        if not current_user.is_authenticated:
            if dash.unauthorized_access:
                dashboards += [dash]
                continue
            else:
                continue
        for role in dash.role:
            for user in role.user:
                if user.id == current_user.id:
                    dashboards += [dash]
    return dashboards
