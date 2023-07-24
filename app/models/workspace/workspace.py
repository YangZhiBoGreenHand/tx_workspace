
from app.base import db
from datetime import datetime


class Workspace(db.Model):
    __tablename__ = 'workspaces'

    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    tenant_id = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow, onupdate=datetime.utcnow)
    ui_settings = db.Column(db.JSON, default={})
    order = db.Column(db.Integer)
    create_by = db.Column(db.String(255))
    deleted_at = db.Column(db.DateTime, default=None)

    def __repr__(self):
        return f'<Workspace {self.id}>'
