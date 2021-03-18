from functools import wraps
from urllib.parse import urlparse

from flask import request, redirect
from flask.helpers import url_for
from flask_login import current_user
from werkzeug.exceptions import HTTPException

from app.models import Dashboard
from app.logger import log


def verify_role_dash(route_method):
    @wraps(route_method)
    def wrapper(*args, **kwargs):
        assert request
        url = request.base_url
        url_path = urlparse(url).path
        dashboards = Dashboard.query.filter(Dashboard.url.ilike(f"%{url_path}")).all()
        if not dashboards:
            log(log.WARNING, "Can not find dashboard for url:[%s]", url)
            raise HTTPException(
                description=f"Access denied for unknown dashboard URL {url}"
            )
        for dash in dashboards:
            dash_url_path = urlparse(dash.url).path
            if dash_url_path != url_path:
                continue
        if not current_user.is_authenticated:
            if dash.available_to_unregistered_user:
                return route_method(*args, **kwargs)
            log(log.WARNING, "Access denied for unauthorized user")
            raise HTTPException(description="Access denied for unauthorized user")
        if current_user.authenticated:
            if dash.available_to_registered_user:
                return route_method(*args, **kwargs)
        if dash.role:
            for role in dash.role:
                for user in role.user:
                    if user.id == current_user.id:
                        return route_method(*args, **kwargs)
        else:
            return redirect(url_for("main.index"))
        log(log.WARNING, "Access denied for [%s]", current_user.role.name)
        raise HTTPException(description=f"Access denied for {current_user.role.name}")

    return wrapper
