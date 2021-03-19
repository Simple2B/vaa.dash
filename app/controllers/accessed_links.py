from flask_login import current_user
from app.models import Dashboard


def accessed_links():
    dashboards = []
    for dash in Dashboard.query.all():
        if not current_user.is_authenticated:
            if dash.available_to_unregistered_user:
                dashboards += [dash]
                continue
            else:
                continue
        for role in dash.role:
            for user in role.user:
                if user.id == current_user.id:
                    dashboards += [dash]
        if current_user.authenticated:
            if dash.available_to_registered_user:
                dashboards += [dash]
                continue
            else:
                continue

    return set(dashboards)
