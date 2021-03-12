from app import db

from app.models import User
from app.models.utils import ModelMixin


class Role(db.Model, ModelMixin):
    tablename = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
