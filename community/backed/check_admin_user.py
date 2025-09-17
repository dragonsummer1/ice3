from models.db import db
from models.user import User
from app import create_app

if __name__ == '__main__':
    app = create_app('development')
    with app.app_context():
        admin = User.query.filter_by(username='admin').first()
        print(f'管理员用户存在: {admin is not None}')
        if admin:
            print(f'is_admin状态: {admin.is_admin}, 状态: {admin.status}')
            print(f'用户ID: {admin.id}')
            print(f'邮箱: {admin.email}')