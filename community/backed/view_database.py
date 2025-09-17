import sqlite3
import os

# 获取数据库文件路径
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'community_forum.db')

print(f'正在连接数据库: {db_path}')

# 连接到SQLite数据库
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 查看所有表
print("\n数据库中的所有表:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
for table in tables:
    print(f'- {table[0]}')

# 查看users表的内容
print("\nusers表的内容:")
cursor.execute("SELECT id, username, is_admin, status FROM users;")
users = cursor.fetchall()
print("ID | 用户名 | 是否管理员 | 状态")
print("---|-------|----------|-----|")
for user in users:
    print(f'{user[0]} | {user[1]} | {user[2]} | {user[3]}')

# 查看topics表的内容
print("\ntopics表的内容:")
cursor.execute("SELECT id, title, user_id, status FROM topics;")
topics = cursor.fetchall()
print("ID | 标题 | 用户ID | 状态")
print("---|-----|-------|-----|")
for topic in topics:
    print(f'{topic[0]} | {topic[1][:20]}... | {topic[2]} | {topic[3]}')

# 查看comments表的内容
print("\ncomments表的内容:")
cursor.execute("SELECT id, content, user_id, status FROM comments LIMIT 10;")
comments = cursor.fetchall()
print("ID | 内容 | 用户ID | 状态")
print("---|-----|-------|-----|")
for comment in comments:
    print(f'{comment[0]} | {comment[1][:20]}... | {comment[2]} | {comment[3]}')

# 关闭连接
conn.close()
print("\n数据库连接已关闭")