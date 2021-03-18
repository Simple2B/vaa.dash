#!/user/bin/env python
import click

from app import create_app, db, models, forms
from app.admin_page import init_admin

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


@app.cli.command()
def create_db():
    """Create the configured database."""
    _init_db()


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
