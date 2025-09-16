from models.db import db
from models.topic import Topic
from models.user import User
from models.comment import Comment
from datetime import datetime, timedelta
from app import create_app
import random

# 创建应用实例
app = create_app('development')

# 测试评论内容池
TEST_COMMENTS = [
    "这个地方真的太美了，我去年也去过！强烈推荐大家去看看日出。",
    "请问一下，你们是几月份去的？我计划明年春天去。",
    "攻略写得很详细，谢谢分享！",
    "照片拍得太棒了，用什么相机拍的呀？",
    "我也想去这个地方，请问那边的住宿条件怎么样？",
    "补充一点，当地的美食也很有特色，一定要尝尝！",
    "请问需要提前预订门票吗？",
    "感谢分享！这个地方已经加入我的旅行清单。",
    "我上个月刚从那里回来，确实值得一去。",
    "有没有当地的交通攻略可以分享一下？",
    "这个季节去会不会太冷？需要带什么衣服？",
    "太赞了！期待看到更多这样的分享。",
    "请问带小孩去方便吗？",
    "这个地方的游客多吗？会不会很拥挤？",
    "拍的照片真的太美了，让我更加向往了！",
    "请问那边的消费高吗？",
    "有没有什么特别需要注意的地方？",
    "我也计划去这里，希望能遇到好天气。",
    "攻略很实用，已经收藏了，谢谢！",
    "这个地方在哪个季节去最合适呢？"
]

# 为每个话题添加的评论数量范围
MIN_COMMENTS_PER_TOPIC = 3
MAX_COMMENTS_PER_TOPIC = 8

# 生成随机日期的函数
def get_random_date(base_date):
    # 在基础日期的前后30天内随机生成日期
    days_diff = random.randint(-30, 30)
    return base_date + timedelta(days=days_diff)

# 添加测试评论
with app.app_context():
    print('开始添加测试评论数据...')
    
    # 获取所有活跃用户
    users = User.query.filter_by(status='active').all()
    if not users:
        print('没有找到活跃用户，请先创建用户')
        exit()
    
    # 获取所有话题
    topics = Topic.query.all()
    if not topics:
        print('没有找到话题，请先创建话题')
        exit()
    
    # 记录添加的评论数量
    added_comments = 0
    
    # 为每个话题添加随机数量的评论
    for topic in topics:
        # 随机决定要添加的评论数量
        num_comments = random.randint(MIN_COMMENTS_PER_TOPIC, MAX_COMMENTS_PER_TOPIC)
        
        # 基础日期为话题创建日期
        base_date = topic.created_at
        
        # 为当前话题添加评论
        for _ in range(num_comments):
            # 随机选择一个用户
            user = random.choice(users)
            
            # 随机选择一条评论内容
            content = random.choice(TEST_COMMENTS)
            
            # 生成随机的评论日期（在话题创建日期前后）
            created_at = get_random_date(base_date)
            
            # 创建评论
            comment = Comment(
                content=content,
                user_id=user.id,
                topic_id=topic.id,
                created_at=created_at,
                status='approved'  # 直接设置为已批准状态
            )
            
            # 添加到数据库
            db.session.add(comment)
            added_comments += 1
        
        # 更新话题的回复数和最后回复时间
        topic.replies += num_comments
        topic.last_reply_time = datetime.utcnow()
        
    # 提交更改
    db.session.commit()
    
    print(f'已成功添加 {added_comments} 条测试评论数据！')
    print('评论数据添加完成！')