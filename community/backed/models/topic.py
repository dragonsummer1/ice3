from datetime import datetime
from models.db import db
from datetime import datetime

class Topic(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    views = db.Column(db.Integer, default=0)
    replies = db.Column(db.Integer, default=0)
    last_reply_time = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, published, blocked
    
    # 关系
    author = db.relationship('User', backref=db.backref('topics', lazy=True))
    # 与评论的关系
    comments = db.relationship('Comment', backref='topic', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'user_id': self.user_id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None,
            'views': self.views,
            'replies': self.replies,
            'last_reply_time': self.last_reply_time.strftime('%Y-%m-%d %H:%M:%S') if self.last_reply_time else None,
            'author': self.author.username if self.author else '未知用户',
            'status': self.status,
            'user': {'username': self.author.username if self.author else '未知用户'} if self.author else None
        }