from models.db import db
from models.topic import Topic
from app import create_app

# 创建应用实例
app = create_app('development')

# 在应用上下文中查询数据库
with app.app_context():
    # 查询所有话题
    topics = Topic.query.all()
    
    # 打印话题数量
    print(f"数据库中话题数量: {len(topics)}")
    
    # 打印每个话题的信息
    for topic in topics:
        print(f"ID: {topic.id}, 标题: {topic.title}, 用户ID: {topic.user_id}")