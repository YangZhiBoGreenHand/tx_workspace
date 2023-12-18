from app.base import db
from sqlalchemy import Index
from sqlalchemy.orm import relationship
from app.models.base_models.base_model import BaseModel


class History(BaseModel):
    __tablename__ = 'history'

    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    question = db.Column(db.Text)
    answer = db.Column(db.Text)

    # 添加 history 表的 topic_id 和 user_id 联合索引
    __table_args__ = (Index('idx_topic_user_history', 'topic_id', 'user_id'),)
