from app import create_app
from models.db import db
from models.user import User
from models.comment import Comment

# 创建应用实例
app = create_app('development')

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
    
    print('数据库初始化完成！')
    print('请使用以下账号登录：')
    print('管理员账号: admin / admin123')
    print('测试账号: testuser / testpassword123')
    print('请在首次登录后修改密码以保证安全。')