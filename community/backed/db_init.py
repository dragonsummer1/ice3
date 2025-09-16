import os
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# 创建独立的Flask应用实例
app = Flask(__name__)

# 配置应用
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化SQLAlchemy
db = SQLAlchemy(app)

# 定义模型（为了避免导入冲突，这里重新定义必要的模型）
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='active')
    
    # 设置密码
    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)

class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = db.Column(db.String(20), default='approved')  # approved, pending, deleted
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

# 初始化数据库
with app.app_context():
    print('开始初始化数据库...')
    
    # 创建所有表
    db.create_all()
    
    # 检查是否存在管理员用户
    admin = User.query.filter_by(is_admin=True).first()
    if not admin:
        # 创建默认管理员用户
        admin = User(
            username='admin',
            email='admin@example.com',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('默认管理员用户已创建：username=admin, password=admin123')
    else:
        print('管理员用户已存在')
    
    # 创建一个普通测试用户
    test_user = User.query.filter_by(username='testuser').first()
    if not test_user:
        test_user = User(
            username='testuser',
            email='testuser@example.com'
        )
        test_user.set_password('testpassword123')
        db.session.add(test_user)
        db.session.commit()
        print('测试用户已创建：username=testuser, password=testpassword123')
    
    # 创建一条测试评论
    if Comment.query.count() == 0:
        comment = Comment(
            content='这是一条测试评论',
            user_id=test_user.id
        )
        db.session.add(comment)
        db.session.commit()
        print('测试评论已创建')
    
    print('数据库初始化完成！')
    print('请使用以下账号登录：')
    print('管理员账号: admin / admin123')
    print('测试账号: testuser / testpassword123')
    print('请在首次登录后修改密码以保证安全。')