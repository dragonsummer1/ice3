# 社区论坛后端服务

这是一个基于Flask的社区论坛后端服务，提供用户认证、评论管理和管理员功能。

## 功能特性

### 用户管理
- 用户注册、登录、注销
- 个人信息管理
- 用户状态控制（活跃、禁用等）

### 评论功能
- 发表评论
- 查看评论列表
- 删除自己的评论

### 管理员功能
- 查看所有用户列表
- 查看所有评论列表
- 删除任意评论
- 批量删除评论
- 修改用户状态

## 技术栈

- Python 3.8+
- Flask
- Flask-SQLAlchemy (数据库ORM)
- Flask-Login (用户会话管理)
- SQLite (默认数据库)

## 环境要求

- Python 3.8或更高版本
- pip包管理器

## 安装步骤

1. 克隆项目到本地

```bash
# 假设项目已在本地
cd f:\ice-3\community\backed
```

2. 安装依赖

```bash
pip install -r requirements.txt
```

3. 初始化数据库

```bash
python init_db.py
```

执行此命令后，系统会创建默认管理员账号：
- 用户名: admin
- 密码: admin123

请在首次登录后修改密码以保证安全。

## 运行服务

### 开发环境

```bash
python app.py
```

服务将在 http://127.0.0.1:5000 运行。

### 生产环境

在生产环境中，建议使用WSGI服务器如Gunicorn：

```bash
gunicorn -w 4 'app:create_app("production")'
```

## API 端点

### 用户认证

- `POST /auth/register` - 用户注册
- `POST /auth/login` - 用户登录
- `POST /auth/logout` - 用户注销
- `GET /auth/current-user` - 获取当前用户信息
- `GET /auth/check` - 检查登录状态

### 论坛功能

- `GET /forum/comments` - 获取评论列表
- `POST /forum/comments` - 发表评论
- `DELETE /forum/comments/<id>` - 删除评论
- `GET /forum/my-comments` - 获取当前用户的评论

### 管理员功能

- `GET /admin/users` - 获取用户列表
- `GET /admin/comments` - 获取评论列表
- `DELETE /admin/comments/<id>` - 删除评论
- `POST /admin/comments/batch-delete` - 批量删除评论
- `PUT /admin/users/<id>/status` - 修改用户状态

## 配置说明

配置文件位于 `config.py`，包含以下主要配置：

- `SECRET_KEY` - 应用程序密钥，生产环境应使用随机生成的密钥
- `SQLALCHEMY_DATABASE_URI` - 数据库连接URI
- `DEBUG` - 是否启用调试模式
- `SESSION_COOKIE_SECURE` - 是否启用安全Cookie（生产环境应设为True）

可以通过环境变量覆盖这些配置。

## 注意事项

1. 首次运行前必须执行 `init_db.py` 初始化数据库
2. 生产环境中务必修改默认管理员密码
3. 生产环境中不要使用开发配置
4. 建议使用HTTPS协议部署服务