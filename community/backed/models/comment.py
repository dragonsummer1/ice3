from models.db import db
from datetime import datetime

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
        return {
            'id': self.id,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'status': self.status,
            'user_id': self.user_id,
            'author': {
                'id': self.author.id,
                'username': self.author.username
            }
        }