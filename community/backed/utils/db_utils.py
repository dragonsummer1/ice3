from datetime import datetime, timedelta

# 初始化数据库
def init_db(app):
    with app.app_context():
        # 从app中获取db实例
        from models.db import db
        from models.user import User
        from models.comment import Comment
        
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

# 清理过期数据
def cleanup_expired_data():
    # 从当前应用上下文获取db实例
    from flask import current_app
    from models.comment import Comment
    from models.db import db
    
    with current_app.app_context():
        # 示例：删除30天前的已删除评论
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        deleted_comments = Comment.query.filter(
            Comment.status == 'deleted',
            Comment.updated_at < thirty_days_ago
        ).all()
        
        for comment in deleted_comments:
            db.session.delete(comment)
        db.session.commit()
        
        return len(deleted_comments)

# 统计数据
def get_statistics():
    # 从当前应用上下文获取db实例
    from flask import current_app
    from models.user import User
    from models.comment import Comment
    
    with current_app.app_context():
        # 获取用户总数
        total_users = User.query.count()
        
        # 获取活跃用户数（30天内有活动）
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        active_users = User.query.filter(User.updated_at > thirty_days_ago).count()
        
        # 获取评论总数
        total_comments = Comment.query.count()
        
        # 获取今日新增评论数
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_comments = Comment.query.filter(Comment.created_at >= today).count()
        
        return {
            'total_users': total_users,
            'active_users': active_users,
            'total_comments': total_comments,
            'today_comments': today_comments
        }

# 检查数据库连接
def check_db_connection():
    try:
        # 从当前应用上下文获取db实例
        from flask import current_app
        from models.db import db
        
        with current_app.app_context():
            # 执行简单查询测试连接
            db.session.execute('SELECT 1')
            return True
    except Exception as e:
        print(f'数据库连接错误: {e}')
        return False