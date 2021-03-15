from sqlalchemy_utils import URLType

from app import db
from app.models.utils import ModelMixin
from app.models.role import association_table


class Dashboard(db.Model, ModelMixin):

    __tablename__ = "dashboards"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    description = db.Column(db.String(300))
    url = db.Column(URLType)
    role = db.relationship(
        "Role", back_populates="dashboard", secondary=association_table
    )

    def __repr__(self):
        return "<Dashboard: %s>" % self.title
