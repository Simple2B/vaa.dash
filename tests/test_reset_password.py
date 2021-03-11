import pytest

from tests.utils import register
from app import db, create_app, mail
from app.models import User
from app.controllers import generate_password_reset_url


@pytest.fixture
def client():
    app = create_app(environment="testing")
    app.config["TESTING"] = True

    with app.test_client() as client:
        app_ctx = app.app_context()
        app_ctx.push()
        db.drop_all()
        db.create_all()
        register()
        with mail.record_messages() as outbox:
            client.outbox = outbox
            yield client
        db.session.remove()
        db.drop_all()
        app_ctx.pop()


def test_password_reset(client):
    user = User.query.first()
    email = user.email
    data = {"email": email}
    response = client.post("/reset_password", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert (
        b"An email has been sent with instructions to reset your password"
        in response.data
    )

    # Test email contains proper token in body
    assert len(client.outbox) == 1
    confirm_url = generate_password_reset_url(email)
    assert client.outbox[0].html
    response = client.get(confirm_url, follow_redirects=True)
    assert response.status_code == 200
    user = User.query.filter(User.email == email).first()
    assert user

    data = {"password": "123Testing123", "confirm_password": "123Testing123"}
    response = client.post(confirm_url, data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Your password has been changed!" in response.data
