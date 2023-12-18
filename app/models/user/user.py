from app.base import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Index
from app.models.base_models.base_model import BaseModel

# 定义数据库模型类


class User(BaseModel):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, default=0)
    gender = db.Column(db.String(10))
    avatar = db.Column(db.String(100))
    phone_number = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 添加唯一索引
    __table_args__ = (
        Index('idx_unique_phone_number', 'phone_number', unique=True),
    )
