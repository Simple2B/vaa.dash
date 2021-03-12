import pytest

from app import db, create_app
from tests.utils import register, login, logout


@pytest.fixture
def client():
    app = create_app(environment="testing")
    app.config["TESTING"] = True

    with app.test_client() as client:
        app_ctx = app.app_context()
        app_ctx.push()
        db.drop_all()
        db.create_all()
        yield client
        db.session.remove()
        db.drop_all()
        app_ctx.pop()


def test_auth_pages(client):
    response = client.get("/signup")
    assert response.status_code == 200
    response = client.get("/signin")
    assert response.status_code == 200
    response = client.get("/logout")
    assert response.status_code == 302


def test_register(client):
    response = client.post(
        "/signup",
        data=dict(
            first_name="firstname",
            last_name="lastname",
            email="test@test.com",
            country="UK",
            password="password",
            password_confirmation="password",
        ),
        follow_redirects=True,
    )
    assert response.status_code == 200


def test_login_and_logout(client):
    # Access to logout view before login should fail.
    response = logout(client)
    assert b"Please log in to access this page." in response.data

    register()
    response = login(client, "test@test.com")
    assert response.status_code == 200

    # Should successfully logout the currently logged in user.
    response = logout(client)
    assert response.status_code == 200

    # Incorrect login credentials should fail.
    response = login(client, "sometest@gmail.com", "wrongpassword")
    assert b"Wrong email or password." in response.data

    # Correct credentials should login
    response = login(client, "test@test.com")
    assert response.status_code == 200
