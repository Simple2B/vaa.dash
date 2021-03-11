# from datetime import datetime

from flask_login import UserMixin, AnonymousUserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models.utils import ModelMixin


class User(db.Model, UserMixin, ModelMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    email = db.Column(db.String(255))
    country = db.Column(db.String(50))
    organization = db.Column(db.String(100))
    password_hash = db.Column(db.String(255))
    # activated = db.Column(db.Boolean, default=False)
    # created_at = db.Column(db.DateTime, default=datetime.now)

    @hybrid_property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @classmethod
    def authenticate(cls, email, password):
        user = cls.query.filter(cls.email == email).first()
        if user is not None and check_password_hash(user.password, password):
            return user

    def __str__(self):
        return "<User: %s %s>" % self.first_name, self.last_name


class AnonymousUser(AnonymousUserMixin):
    pass
