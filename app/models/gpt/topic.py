from app.base import db
from sqlalchemy import Index
from sqlalchemy.orm import relationship
from app.models.base_models.base_model import BaseModel


class Topic(BaseModel):
    __tablename__ = 'topics'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer)

    # 添加唯一索引
    __table_args__ = (Index('idx_user_id_topics', 'user_id'),)
