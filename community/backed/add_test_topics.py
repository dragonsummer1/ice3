from flask import Flask
from models.db import db
from models.topic import Topic
from models.user import User
from datetime import datetime, timedelta
import random
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入create_app函数
from app import create_app

# 测试话题标题和内容
TEST_TOPICS = [
    {
        'title': '分享一次难忘的旅行经历',
        'content': '上个月去了云南，那里的风景真的太美了！特别是丽江古城和大理洱海，让人流连忘返。建议大家有机会一定要去看看。',
        'category': '景点',
        'status': 'published'
    },
    {
        'title': '出国旅行必备物品清单',
        'content': '1. 护照和签证文件\n2. 转换插头\n3. 充电宝\n4. 常用药品\n5. 少量现金\n6. 旅行保险凭证',
        'category': '其他',
        'status': 'pending'
    },
    {
        'title': '如何选择合适的旅行保险',
        'content': '在选择旅行保险时，需要考虑以下几点：\n- 保障范围\n- 医疗保障额度\n- 紧急救援服务\n- 免责条款\n- 价格比较',
        'category': '其他',
        'status': 'published'
    },
    {
        'title': '日本东京自由行攻略',
        'content': '东京是一个充满活力的城市，推荐行程：\nDay 1: 浅草寺 → 晴空塔 → 秋叶原\nDay 2: 明治神宫 → 原宿 → 涩谷\nDay 3: 迪士尼乐园一日游\nDay 4: 台场 → 东京塔夜景',
        'category': '交通',
        'status': 'pending'
    },
    {
        'title': '三亚住宿推荐',
        'content': '去三亚旅游，推荐住在亚龙湾或海棠湾，这里的酒店设施好，海滩质量高。预算充足的话可以考虑亚特兰蒂斯或丽思卡尔顿。',
        'category': '住宿',
        'status': 'blocked'
    },
    {
        'title': '泰国清迈必吃美食',
        'content': '清迈的美食种类繁多，推荐尝试：\n1. 青咖喱鸡\n2. 冬阴功汤\n3. 芒果糯米饭\n4. 泰式炒河粉\n5. 青木瓜沙拉',
        'category': '美食',
        'status': 'published'
    },
    {
        'title': '欧洲自助游签证攻略',
        'content': '申请申根签证的步骤：\n1. 确定主申请国\n2. 准备申请材料\n3. 在线预约\n4. 面签\n5. 等待结果\n一般建议提前1-2个月申请。',
        'category': '其他',
        'status': 'pending'
    }
]

# 为用户添加测试话题
def add_test_topics():
    # 创建应用实例
    app = create_app('development')  # 使用开发环境配置
    
    with app.app_context():
        # 获取所有用户
        users = User.query.all()
        
        if not users:
            print("没有找到用户，请先创建用户")
            return
        
        # 计算要添加的话题数量
        existing_topics = Topic.query.count()
        topics_to_add = len(TEST_TOPICS) - existing_topics
        
        if topics_to_add <= 0:
            print("已经有足够的测试话题数据")
            return
        
        print(f"准备添加 {topics_to_add} 个测试话题")
        
        added_count = 0
        
        for topic_data in TEST_TOPICS:
            # 检查是否已存在相同标题的话题
            existing_topic = Topic.query.filter_by(title=topic_data['title']).first()
            if existing_topic:
                continue
            
            # 随机选择一个用户作为作者
            user = random.choice(users)
            
            # 创建随机的创建时间（过去7天内）
            days_ago = random.randint(0, 7)
            created_at = datetime.utcnow() - timedelta(days=days_ago)
            
            # 创建话题
            topic = Topic(
                title=topic_data['title'],
                content=topic_data['content'],
                category=topic_data['category'],
                user_id=user.id,
                created_at=created_at,
                updated_at=created_at,
                status=topic_data['status'],
                views=random.randint(0, 100)
            )
            
            db.session.add(topic)
            added_count += 1
            
            print(f"添加话题: {topic_data['title']} (作者: {user.username}, 状态: {topic_data['status']})")
        
        # 提交更改
        db.session.commit()
        
        print(f"成功添加了 {added_count} 个测试话题")

if __name__ == '__main__':
    add_test_topics()