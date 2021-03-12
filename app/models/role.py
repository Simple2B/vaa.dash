from app import db

from app.models.utils import ModelMixin


association_table = db.Table(
    "role_dashboard",
    db.metadata,
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id")),
    db.Column("dashboard_id", db.Integer, db.ForeignKey("dashboards.id")),
)


class Role(db.Model, ModelMixin):

    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    user = db.relationship("User")
    dashboard = db.relationship(
        "Dashboard", back_populates="role", secondary=association_table
    )

    def __repr__(self):
        return "<Role: %s>" % self.name
