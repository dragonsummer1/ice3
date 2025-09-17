# Ice Travel Community 项目启动指南

本指南提供了启动 Ice Travel Community 项目的详细步骤，包括前端 Vue 3 应用和后端 Flask 服务的完整配置与运行说明。

## 项目概述

Ice Travel Community 是一个哈尔滨旅游论坛系统，允许用户发布旅游攻略、结伴同行、讨论景点和美食等话题，并支持管理员审核内容。

## 项目结构详解

```
├── backed/           # 后端 Flask 项目
│   ├── app.py        # Flask 应用入口
│   ├── config.py     # 配置文件
│   ├── models/       # 数据模型
│   ├── routes/       # API 路由
│   ├── utils/        # 工具函数
│   ├── db_init.py    # 数据库初始化脚本
│   └── requirements.txt # Python 依赖列表
├── src/              # 前端 Vue 项目源代码
│   ├── views/        # 页面组件
│   ├── components/   # 可复用组件
│   ├── stores/       # Pinia 状态管理
│   ├── router.js     # Vue Router 配置
│   └── main.js       # Vue 应用入口
├── public/           # 静态资源
├── package.json      # 前端依赖配置
└── vite.config.js    # Vite 构建配置
```

## 前提条件

在启动项目前，请确保您已安装以下软件：

- [Node.js](https://nodejs.org/) (v14 或更高版本)
- [npm](https://www.npmjs.com/) (v6 或更高版本)
- [Python](https://www.python.org/) (v3.8 或更高版本)
- [pip](https://pip.pypa.io/en/stable/) (Python 包管理器，通常随 Python 一起安装)
- 建议使用 [Git](https://git-scm.com/) 进行版本控制

## 前端项目启动

### 1. 安装前端依赖

打开命令行工具 (如 Windows 的 PowerShell 或 macOS/Linux 的 Terminal)，进入项目根目录，执行以下命令安装前端依赖：

```bash
# Windows 用户
cd h:\ice-min\community
npm install

# macOS/Linux 用户
cd /path/to/ice-min/community
npm install
```

### 2. 启动前端开发服务器

依赖安装完成后，执行以下命令启动前端开发服务器：

```bash
npm run dev
```

启动成功后，您可以通过浏览器访问以下地址查看前端应用：

- 开发服务器默认地址：http://localhost:5173/

### 3. 构建生产版本

如果需要构建生产环境的优化版本，执行以下命令：

```bash
npm run build
```

构建完成后，优化后的生产文件将生成在 `dist` 目录中。

### 4. 预览生产版本

要预览构建后的生产版本，可以使用以下命令：

```bash
npm run preview
```

预览服务器默认地址：http://localhost:4173/

## 后端项目启动

### 1. 进入后端目录

打开新的命令行窗口，进入项目的后端目录：

```bash
# Windows 用户
cd h:\ice-min\community\backed

# macOS/Linux 用户
cd /path/to/ice-min/community/backed
```

### 2. 创建并激活虚拟环境 (推荐)

为了隔离项目依赖，强烈建议创建一个 Python 虚拟环境：

```bash
# Windows 环境
python -m venv venv
# 激活虚拟环境 (PowerShell)
venv\Scripts\Activate.ps1
# 或 (CMD)
venv\Scripts\activate.bat

# macOS/Linux 环境
python3 -m venv venv
# 激活虚拟环境
source venv/bin/activate
```

### 3. 安装后端依赖

在激活虚拟环境的状态下，执行以下命令安装后端依赖：

```bash
pip install -r requirements.txt
```

### 4. 初始化数据库

首次运行项目时，需要初始化数据库：

```bash
# Windows 环境
python db_init.py

# macOS/Linux 环境
python3 db_init.py
```

此命令会创建 SQLite 数据库文件 `instance/ice_travel_community.db` 并初始化所有必要的表结构。

### 5. 生成测试数据 (可选)

如果需要添加测试数据，可以运行以下脚本：

```bash
# 添加测试话题
python add_test_topics.py

# 添加测试评论
python add_test_comments.py
```

### 6. 启动后端服务器

数据库初始化完成后，执行以下命令启动后端 Flask 服务器：

```bash
# Windows 环境 (PowerShell)
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"
flask run

# Windows 环境 (CMD)
set FLASK_APP=app.py
set FLASK_ENV=development
flask run

# macOS/Linux 环境
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

后端服务器默认将在以下地址运行：
- http://localhost:5000/

## 同时启动前后端服务

要同时运行完整的应用程序，您需要打开两个独立的命令行窗口：

1. **第一个窗口**：运行前端开发服务器
   ```bash
   npm run dev
   ```

2. **第二个窗口**：运行后端 Flask 服务器
   ```bash
   # 确保已进入 backed 目录并激活虚拟环境
   flask run
   ```

## 环境变量配置

后端项目使用 `.env` 文件配置环境变量。在 `backed` 目录中创建一个 `.env` 文件，并添加以下内容：

```env
# Flask 应用配置
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# 数据库配置
SQLALCHEMY_DATABASE_URI=sqlite:///instance/ice_travel_community.db
SQLALCHEMY_TRACK_MODIFICATIONS=False

# 调试模式
DEBUG=True
TESTING=False
```

> **注意**：在生产环境中，应使用强密码作为 `SECRET_KEY`，并将 `DEBUG` 和 `TESTING` 设置为 `False`。

## 跨域配置说明

项目已配置 CORS 支持，以允许前端应用访问后端 API。默认配置允许来自以下源的请求：
- http://localhost:5173 (前端开发服务器)
- http://localhost:5174 (备用开发端口)

如果您需要修改这些配置，请编辑 `backed/app.py` 文件中的 CORS 配置部分。

## 常见问题及解决方案

### 1. 端口冲突

如果 5173 或 5000 端口已被其他程序占用，您需要修改端口设置：

- **前端端口修改**：
  在 `package.json` 文件中修改 `scripts.dev` 命令：
  ```json
  "scripts": {
    "dev": "vite --port 5174"
  }
  ```
  或创建一个 `vite.config.js` 文件，添加端口配置。

- **后端端口修改**：
  ```bash
  flask run --port 5001
  ```

### 2. 依赖安装失败

- **前端依赖问题**：
  ```bash
  # 清除 npm 缓存
  npm cache clean --force
  
  # 重新安装依赖
  npm install
  ```

- **后端依赖问题**：
  ```bash
  # 升级 pip
  pip install --upgrade pip
  
  # 重新安装依赖
  pip install -r requirements.txt
  ```

### 3. 数据库连接问题

- 确保数据库文件 `instance/ice_travel_community.db` 有正确的读写权限
- 尝试重新初始化数据库：
  ```bash
  python force_db_reinit.py
  python db_init.py
  ```

### 4. CORS 错误

如果前端应用无法访问后端 API 并出现 CORS 错误：
- 确保前端应用运行在允许的源地址（如 http://localhost:5173）
- 检查 `backed/app.py` 中的 CORS 配置是否包含了您使用的前端地址
- 确认 `Access-Control-Allow-Credentials` 设置为 `true`

### 5. 服务启动失败

- 检查日志信息以获取具体错误
- 确认所有依赖都已正确安装
- 对于 Windows 用户，确保在 PowerShell 中以管理员身份运行命令

## 开发流程建议

1. **启动开发环境**：
   - 先启动后端服务器
   - 再启动前端开发服务器

2. **代码修改**：
   - 前端代码修改会触发 Vite 的热模块替换，无需手动刷新页面
   - 后端代码修改后，需要重新启动 Flask 服务器以应用更改

3. **测试数据**：
   - 使用提供的测试脚本快速生成测试数据
   - 或手动创建用户并发布内容进行测试

## 生产部署建议

1. **前端部署**：
   - 运行 `npm run build` 生成生产版本
   - 将 `dist` 目录中的文件部署到静态文件服务器（如 Nginx、Apache）

2. **后端部署**：
   - 使用 Gunicorn 或 uWSGI 作为 WSGI 服务器
   - 配置反向代理（如 Nginx）处理静态文件和请求转发
   - 设置适当的环境变量（禁用 DEBUG 模式）

3. **数据库**：
   - 对于生产环境，考虑使用 PostgreSQL 或 MySQL 替代 SQLite

---

完成以上步骤后，您应该能够成功启动 Ice Travel Community 项目的前端和后端服务。如有其他问题，请参考项目文档或联系开发团队。