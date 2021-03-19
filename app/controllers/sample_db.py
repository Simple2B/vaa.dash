# flake8: noqa F841
from app.models import User, Dashboard, Role


def register_user(
    first_name,
    last_name,
    email,
    country,
    organization,
    password="password",
):
    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        country=country,
        organization=organization,
    )
    user.set_password(password)
    user.save()
    return user.id


def create_dashboard(
    title,
    descriprion,
    url,
    roles,
    available_to_unregistered_user=False,
    available_to_registered_user=False,
):
    dashboard = Dashboard(
        title=title,
        description=descriprion,
        url=url,
        available_to_unregistered_user=available_to_unregistered_user,
        available_to_registered_user=available_to_registered_user,
    )
    dashboard.role += roles
    return dashboard.save()


def create_user_with_role(
    role_name,
    first_name,
    last_name,
    email,
    country,
    organization,
):
    role = Role(name=role_name).save()
    user_id = register_user(first_name, last_name, email, country, organization)
    user = User.query.get(user_id)
    user.role = role
    return user.save()


def filled_db():

    """Create users with rolee"""
    admin_user = create_user_with_role(
        "admin_role", "Admin", "User", "admin@test.com", "USA", "WWW"
    )

    user_with_a_certain_role = create_user_with_role(
        "user_with_a_certain_role",
        "Just",
        "User",
        "userwithrole@test.com",
        "USA",
        "HHH",
    )

    """Dashboards"""
    dash1 = create_dashboard(
        "Clinical Analytics",
        "Explore clinic patient volume by time of day, waiting time, and care score. Click on the heatmap to visualize patient experience at different time points.",
        "http://127.0.0.1:5000/the_first_dash_app",
        [admin_user.role],
        available_to_unregistered_user=True,
        available_to_registered_user=True,
    )
    dash2 = create_dashboard(
        "The Yield Curve",
        "The yield curve shows how much it costs the federal government to borrow money for a given amount of time, revealing the relationship between long- and short-term interest rates.",
        "http://127.0.0.1:5000/the_second_dash_app",
        [user_with_a_certain_role.role],
        available_to_unregistered_user=True,
        available_to_registered_user=False,
    )
    dash3 = create_dashboard(
        "New York Oil and Gas",
        "New York Oil and Gas Production Overview",
        "http://127.0.0.1:5000/the_third_dash_app",
        [admin_user.role, user_with_a_certain_role.role],
        available_to_unregistered_user=False,
        available_to_registered_user=False,
    )

    return
