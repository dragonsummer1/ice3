from datetime import datetime
from models.db import db
from models.user import User

class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = db.Column(db.String(20), default='approved')  # approved, pending, deleted
    
    # 外键：关联到用户表
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # 外键：关联到话题表
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    
    # 转换为字典格式
    def to_dict(self):
        # 直接通过user_id从数据库获取正确的用户信息
        user = User.query.get(self.user_id)
        user_id = user.id if user else self.user_id
        username = user.username if user else '未知用户'
        
        return {
            'id': self.id,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'status': self.status,
            'user_id': user_id,
            'author': {
                'id': user_id,
                'username': username
            }
        }