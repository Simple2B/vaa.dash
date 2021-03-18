from app.models import User, Role, Dashboard


def register(
    first_name="firstname",
    last_name="lastname",
    email="test@test.com",
    country="UK",
    authenticated=False,
    password="password",
):
    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        country=country,
        authenticated=authenticated,
    )
    user.set_password(password)
    user.save()
    return user.id


def create_dashboard(title, descriprion, url, roles, unauthorized_access=False):
    dashboard = Dashboard(
        title=title,
        description=descriprion,
        url=url,
        unauthorized_access=unauthorized_access,
    )
    dashboard.role += roles
    return dashboard.save()


def create_test_user(role_name, user_name):
    role = Role(name=role_name).save()
    user_id = register(user_name, user_name, f"{user_name}@test.com")
    user = User.query.get(user_id)
    user.role = role
    return user.save()


def filled_db():
    """Types of users"""
    admin_user = create_test_user("admin", "admin")
    user = create_test_user("user", "user")
    authenticated_user = create_test_user("authenticated_user", "authenticated_user")

    """Dashboards"""
    dash1 = create_dashboard(
        "dash1",
        "description for dash1",
        "http://127.0.0.1:5000/dash_app_1",
        [admin_user.role],
        unauthorized_access=True,
    )
    dash2 = create_dashboard(
        "dash2",
        "description for dash2",
        "http://127.0.0.1:5000/dash_app_2",
        [user.role],
    )
    dash3 = create_dashboard(
        "dash3",
        "description for dash3",
        "http://127.0.0.1:5000/dash_app_3",
        [authenticated_user.role],
    )
    return


def login(client, email, password="password"):
    return client.post(
        "/signin", data=dict(email=email, password=password), follow_redirects=True
    )


def login_admin(client, email="admin@test.com", password="password"):
    return client.post(
        "/signin", data=dict(email=email, password=password), follow_redirects=True
    )


def logout(client):
    return client.get("/logout", follow_redirects=True)
