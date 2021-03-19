#!/user/bin/env python
import click

from app import create_app, db, models, forms
from app.admin_page import init_admin
from app.controllers import filled_db

app = create_app()
admin_page = init_admin(app, db)


# flask cli context setup
@app.shell_context_processor
def get_context():
    """Objects exposed here will be automatically available from the shell."""
    return dict(app=app, db=db, models=models, forms=forms)


# create db
def _init_db():
    db.create_all()


# create an empty db
@app.cli.command()
def create_db():
    """Create the configured database."""
    _init_db()


# create a db with a test data
@app.cli.command()
def create_db_with_data():
    """Create the configured database with a test data."""
    _init_db()
    filled_db()


@app.cli.command()
@click.confirmation_option(prompt="Delete all data from database tables?")
def reset_db():
    """Reset the current database."""
    db.drop_all()
    _init_db()


@app.cli.command()
@click.confirmation_option(prompt="Drop all database tables?")
def drop_db():
    """Drop the current database."""
    db.drop_all()


if __name__ == "__main__":
    app.run()
