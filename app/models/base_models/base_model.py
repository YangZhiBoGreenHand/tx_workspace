from app.base import db
from datetime import datetime


class BaseModel(db.Model):
    __abstract__ = True  # 声明这是一个抽象基类，不会在数据库中创建表

    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow, onupdate=datetime.utcnow)
