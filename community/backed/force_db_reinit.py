import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime
import os

# 创建独立的Flask应用实例
app = Flask(__name__)

# 配置数据库
app.config['SECRET_KEY'] = 'dev-secret-key'

# SQLite数据库文件
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'community_forum.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
new_db = SQLAlchemy(app)

# 定义User模型
class User(new_db.Model):
    __tablename__ = 'users'
    
    id = new_db.Column(new_db.Integer, primary_key=True)
    username = new_db.Column(new_db.String(80), unique=True, nullable=False)
    email = new_db.Column(new_db.String(120), unique=True, nullable=False)
    password_hash = new_db.Column(new_db.String(200), nullable=False)
    created_at = new_db.Column(new_db.DateTime, default=datetime.utcnow)
    updated_at = new_db.Column(new_db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_admin = new_db.Column(new_db.Boolean, default=False)
    status = new_db.Column(new_db.String(20), default='active')
    
    # 设置密码
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

# 定义Comment模型
class Comment(new_db.Model):
    __tablename__ = 'comments'
    
    id = new_db.Column(new_db.Integer, primary_key=True)
    content = new_db.Column(new_db.Text, nullable=False)
    created_at = new_db.Column(new_db.DateTime, default=datetime.utcnow)
    updated_at = new_db.Column(new_db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = new_db.Column(new_db.String(20), default='approved')  # approved, pending, deleted
    user_id = new_db.Column(new_db.Integer, new_db.ForeignKey('users.id'), nullable=False)
    topic_id = new_db.Column(new_db.Integer, new_db.ForeignKey('topics.id'))

# 定义Topic模型
class Topic(new_db.Model):
    __tablename__ = 'topics'
    
    id = new_db.Column(new_db.Integer, primary_key=True)
    title = new_db.Column(new_db.String(100), nullable=False)
    content = new_db.Column(new_db.Text, nullable=False)
    category = new_db.Column(new_db.String(50), nullable=False)
    user_id = new_db.Column(new_db.Integer, new_db.ForeignKey('users.id'), nullable=False)
    created_at = new_db.Column(new_db.DateTime, default=datetime.utcnow)
    updated_at = new_db.Column(new_db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    views = new_db.Column(new_db.Integer, default=0)
    replies = new_db.Column(new_db.Integer, default=0)
    last_reply_time = new_db.Column(new_db.DateTime, default=datetime.utcnow)

def main():
    print("开始强制重新初始化数据库...")
    
    # 对于SQLite数据库，我们需要删除现有数据库文件
    print(f"数据库文件路径: {db_path}")
    
    # 检查并删除现有数据库文件
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print(f"已删除现有数据库文件: {db_path}")
        except Exception as e:
            print(f"删除数据库文件失败: {e}")
            print("请确保程序有足够的权限删除文件，或者文件没有被其他进程占用。")
            return
    else:
        print("数据库文件不存在，将创建新的数据库文件。")
        
    # 确保instance目录存在
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # 在应用上下文中创建所有表
    with app.app_context():
        # 创建所有表
        new_db.create_all()
        print("所有数据库表已重新创建")
        
        # 创建管理员用户
        admin = User(username='admin', email='admin@example.com', is_admin=True)
        admin.set_password('admin123')
        new_db.session.add(admin)
        
        # 创建测试用户
        test_user = User(username='testuser', email='test@example.com')
        test_user.set_password('testpassword123')
        new_db.session.add(test_user)
        
        # 创建测试评论
        comment1 = Comment(content='这是一条测试评论', user_id=1)
        comment2 = Comment(content='这是另一条测试评论', user_id=2)
        new_db.session.add_all([comment1, comment2])
        
        # 创建测试话题
        topic1 = Topic(title='欢迎来到社区论坛', content='这是一个测试话题，欢迎大家在这里交流分享。', category='其他', user_id=1)
        topic2 = Topic(title='分享我的旅行经历', content='刚刚结束了一次美好的旅行，想和大家分享一下我的见闻。', category='景点', user_id=2)
        new_db.session.add_all([topic1, topic2])
        
        # 提交更改
        new_db.session.commit()
        
        print("数据库初始化完成！")
        print("请使用以下账号登录：")
        print("管理员账号: admin / admin123")
        print("测试账号: testuser / testpassword123")
        print("请在首次登录后修改密码以保证安全。")

if __name__ == '__main__':
    main()