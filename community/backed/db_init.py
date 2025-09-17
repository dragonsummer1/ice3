# 导入必要的模块
import os
from flask import Flask

# 创建应用实例
app = Flask(__name__)

# 配置应用 - 使用与config.py相同的数据库路径
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'instance', 'community_forum.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 导入数据库和所有必要的模型
from models.db import db
from models.user import User
from models.topic import Topic
from models.comment import Comment

# 初始化数据库扩展
db.init_app(app)

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