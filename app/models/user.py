from datetime import datetime

from flask_login import UserMixin, AnonymousUserMixin
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
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    password_hash = db.Column(db.String(255))
    authenticated = db.Column(db.Boolean, default=False)
    signup_at = db.Column(db.DateTime, default=datetime.now)
    role = db.relationship("Role")

    @property
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def set_password(self, user_password):
        self.password_hash = generate_password_hash(user_password)

    def check_password(self, user_password):
        return check_password_hash(self.password_hash, user_password)

    def __repr__(self):
        return "<User: %s>" % self.email


class AnonymousUser(AnonymousUserMixin):
    @property
    def is_authenticated(self):
        return False

    @property
    def is_active(self):
        return False

    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        return
