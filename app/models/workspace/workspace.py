
from app.base import db
from app.models.base_models.base_model import BaseModel


class Workspace(BaseModel):
    __tablename__ = 'workspaces'

    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    tenant_id = db.Column(db.String(255))
    ui_settings = db.Column(db.JSON, default={})
    order = db.Column(db.Integer)
    create_by = db.Column(db.String(255))
    deleted_at = db.Column(db.DateTime, default=None)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
