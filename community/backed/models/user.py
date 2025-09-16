from models.db import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='active')  # active, banned, suspended
    
    # 关系：用户发表的评论
    comments = db.relationship('Comment', backref='author', lazy=True, cascade='all, delete-orphan')
    
    # 设置密码
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    # 验证密码
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # 转换为字典格式
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'is_admin': self.is_admin,
            'status': self.status
        }
    
    # 检查是否为管理员
    def is_admin_user(self):
        return self.is_admin