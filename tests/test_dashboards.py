import pytest
from app.models import User, Dashboard

from app import db, create_app
from tests.utils import filled_db, login_admin


@pytest.fixture
def client():
    app = create_app(environment="testing")
    app.config["TESTING"] = True

    with app.test_client() as client:
        app_ctx = app.app_context()
        app_ctx.push()
        db.drop_all()
        db.create_all()
        filled_db()
        yield client
        db.session.remove()
        db.drop_all()
        app_ctx.pop()


def test_dashboard_access(client):

    response = login_admin(client)
    assert response
    user = User.query.get(1)
    assert user.first_name == "admin"
    assert user.role.name == "admin"

    admin_dashboard = Dashboard.query.get(1)
    assert admin_dashboard.role[0]
    assert admin_dashboard.role[0].name == user.role.name
    assert admin_dashboard.url

    response = client.get("/the_first_dash_app", follow_redirects=True)
    assert response.status_code
    assert response.status_code == 200
