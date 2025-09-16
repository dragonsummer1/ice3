# Ice Travel Community 项目启动指南

本指南将帮助您启动 Ice Travel Community 项目的前端和后端服务。

## 项目结构概览

```
├── backend/           # 后端 Flask 项目
├── src/               # 前端 Vue 项目源代码
├── package.json       # 前端依赖配置
└── README.md          # 项目说明文档
```

## 前提条件

在启动项目前，请确保您已安装以下软件：

- [Node.js](https://nodejs.org/) (v14 或更高版本)
- [npm](https://www.npmjs.com/) (通常随 Node.js 一起安装)
- [Python](https://www.python.org/) (v3.8 或更高版本)
- [pip](https://pip.pypa.io/en/stable/) (Python 包管理器)

## 前端启动步骤

### 1. 安装依赖

打开命令行工具，进入项目根目录，执行以下命令安装前端依赖：

```bash
npm install
```

### 2. 启动开发服务器

依赖安装完成后，执行以下命令启动前端开发服务器：

```bash
npm run dev
```

前端服务器启动后，您可以通过浏览器访问 http://localhost:5173/ 查看项目。

### 3. 构建生产版本

如果需要构建生产版本，执行以下命令：

```bash
npm run build
```

构建完成后，生产文件将生成在 `dist` 目录中。

## 后端启动步骤

### 1. 进入后端目录

打开新的命令行工具，进入项目的后端目录：

```bash
cd backend
```

### 2. 创建虚拟环境 (可选但推荐)

为了隔离项目依赖，建议创建一个虚拟环境：

```bash
# Windows 环境
python -m venv venv
# 激活虚拟环境
venv\Scripts\Activate.ps1

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

执行以下命令初始化数据库：

```bash
python db_init.py
```

### 5. 启动后端服务器

数据库初始化完成后，执行以下命令启动后端 Flask 服务器：

```bash
flask run
```

后端服务器默认将在 http://localhost:5000/ 上运行。

## 同时启动前后端

要同时启动前后端服务，您需要打开两个命令行窗口：

1. 一个窗口用于运行前端开发服务器 (`npm run dev`)
2. 另一个窗口用于运行后端 Flask 服务器 (`flask run`)

## 常见问题解决

### 1. 端口冲突

如果 5173 或 5000 端口已被占用，您可能需要修改配置文件中的端口设置。

### 2. 依赖安装失败

- 前端：尝试清除 npm 缓存 `npm cache clean --force` 后重新安装
- 后端：检查 Python 和 pip 版本，确保符合要求

### 3. 数据库连接问题

确保数据库文件 `instance/ice_travel_community.db` 有正确的读写权限，并且已通过 `db_init.py` 成功初始化。

## 环境变量配置

后端项目使用 `.env` 文件配置环境变量，确保您的 `.env` 文件包含正确的配置信息。