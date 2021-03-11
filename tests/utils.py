from app.models import User


def register(
    first_name="firstname",
    last_name="lastname",
    email="test@test.com",
    country="UK",
    password="password",
):
    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        country=country,
    )
    user.set_password(password)
    user.save()
    return user.id


def login(client, email, password="password"):
    return client.post(
        "/signin", data=dict(email=email, password=password), follow_redirects=True
    )


def logout(client):
    return client.get("/logout", follow_redirects=True)
