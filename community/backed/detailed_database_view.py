import sqlite3
import os
from datetime import datetime

# 获取数据库文件路径
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'community_forum.db')

print(f'正在连接数据库: {db_path}')

# 连接到SQLite数据库
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 查看待审核的话题
def view_pending_topics():
    print("\n待审核的话题详情:")
    cursor.execute("SELECT t.id, t.title, t.content, t.user_id, u.username, t.status, t.created_at FROM topics t JOIN users u ON t.user_id = u.id WHERE t.status = 'pending';")
    pending_topics = cursor.fetchall()
    if not pending_topics:
        print("没有待审核的话题")
        return
    
    print("ID | 标题 | 创建用户 | 用户ID | 状态 | 创建时间")
    print("---|-----|---------|-------|-----|--------|")
    for topic in pending_topics:
        created_at = datetime.fromisoformat(topic[6]).strftime('%Y-%m-%d %H:%M:%S') if topic[6] else '未知'
        print(f'{topic[0]} | {topic[1][:20]}... | {topic[4]} | {topic[3]} | {topic[5]} | {created_at}')
    
    return pending_topics

# 查看已发布的话题和它们的原始作者
def view_published_topics():
    print("\n已发布的话题详情:")
    cursor.execute("SELECT t.id, t.title, t.content, t.user_id, u.username, t.status, t.created_at FROM topics t JOIN users u ON t.user_id = u.id WHERE t.status = 'published';")
    published_topics = cursor.fetchall()
    
    print("ID | 标题 | 创建用户 | 用户ID | 状态 | 创建时间")
    print("---|-----|---------|-------|-----|--------|")
    for topic in published_topics:
        created_at = datetime.fromisoformat(topic[6]).strftime('%Y-%m-%d %H:%M:%S') if topic[6] else '未知'
        print(f'{topic[0]} | {topic[1][:20]}... | {topic[4]} | {topic[3]} | {topic[5]} | {created_at}')

# 查看评论和它们的原始作者
def view_comments():
    print("\n评论详情:")
    cursor.execute("SELECT c.id, c.content, c.user_id, u.username, c.status, c.created_at FROM comments c JOIN users u ON c.user_id = u.id;")
    comments = cursor.fetchall()
    
    print("ID | 内容 | 创建用户 | 用户ID | 状态 | 创建时间")
    print("---|-----|---------|-------|-----|--------|")
    for comment in comments:
        created_at = datetime.fromisoformat(comment[5]).strftime('%Y-%m-%d %H:%M:%S') if comment[5] else '未知'
        print(f'{comment[0]} | {comment[1][:20]}... | {comment[3]} | {comment[2]} | {comment[4]} | {created_at}')

# 运行查看函数
view_pending_topics()
view_published_topics()
view_comments()

# 关闭连接
conn.close()
print("\n数据库连接已关闭")

print("\n提示：您可以使用以下步骤测试修复是否生效：")
print("1. 以管理员身份登录系统")
print("2. 前往管理界面审核一条待审核的话题")
print("3. 在前台查看该话题，确认作者显示为原始作者而非admin")