# CampusTree 校园树洞匿名交流平台

CampusTree 是一个面向大学生的校园树洞匿名交流平台，采用前后端分离架构。当前版本定位为课程设计可演示 MVP，已经完成用户、帖子、评论、点赞和个人中心等核心功能。

## 当前状态

当前项目已经可以在本地完成完整 MVP 演示，但还不是生产级最终版本。

已完成：

- 用户注册、登录、JWT 身份认证
- 获取当前用户信息
- 修改密码
- 发布帖子、浏览帖子、查看帖子详情
- 修改和删除自己的帖子
- 发布评论、查看评论、删除自己的评论
- 点赞和取消点赞
- 个人中心、我的帖子、我的评论、统计数据
- Vue 前端页面和 FastAPI 后端接口联调
- 后端测试、前端构建和前端 lint 已通过

暂未完成：

- AI 回复、AI 情绪分析等 AI 模块
- Nginx、Systemd、公网域名等生产部署配置
- 管理后台、举报系统、实时聊天等扩展功能

更详细的项目状态请查看：

- `docs/CampusTree 当前项目状态.md`
- `docs/CampusTree 本地环境部署与运行指南.md`
- `docs/API_REFERENCE.md`

## 分支说明

当前仓库分支情况：

- `main`：目前主要是完整后端实现
- `frontend-dev`：当前完整 MVP 版本，包含后端、前端和前后端联调

如果同学需要本地运行完整项目，请优先使用：

```powershell
git checkout frontend-dev
```

最终提交或分享给同学前，建议将 `frontend-dev` 合并到 `main`，让 `main` 成为完整可运行版本。

## 技术栈

### 前端

- Vue 3
- Vite
- TypeScript
- Element Plus
- Pinia
- Axios
- Vue Router

### 后端

- Python 3.11+
- FastAPI
- SQLModel
- Alembic
- JWT
- Uvicorn

### 数据库

- PostgreSQL 16

## 项目结构

```text
CampusTree
├── backend
│   ├── app
│   │   ├── api
│   │   ├── core
│   │   ├── db
│   │   ├── models
│   │   ├── schemas
│   │   ├── services
│   │   └── main.py
│   ├── alembic
│   ├── alembic.ini
│   ├── requirements.txt
│   └── .env.example
├── frontend
│   ├── src
│   │   ├── api
│   │   ├── assets
│   │   ├── components
│   │   ├── router
│   │   ├── stores
│   │   ├── types
│   │   ├── utils
│   │   └── views
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── docs
└── README.md
```

## 本地运行

### 1. 克隆项目并切换分支

```powershell
git clone <你的 GitHub 仓库地址>
cd CampusTree
git checkout frontend-dev
```

如果已经合并到 `main`，则不需要切换分支。

### 2. 创建数据库

本地需要先安装 PostgreSQL，并创建数据库：

```powershell
createdb -U postgres -h 127.0.0.1 -p 5432 campustree
```

数据库名：

```text
campustree
```

### 3. 启动后端

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

打开 `backend/.env`，修改数据库密码和 JWT 密钥。

然后执行数据库迁移并启动服务：

```powershell
alembic upgrade head
uvicorn app.main:app --reload
```

后端地址：

```text
http://127.0.0.1:8000
```

接口文档：

```text
http://127.0.0.1:8000/docs
```

### 4. 启动前端

另开一个终端：

```powershell
cd frontend
npm install
npm run dev
```

前端地址通常为：

```text
http://localhost:5173
```

完整本地部署教程请查看：

```text
docs/CampusTree 本地环境部署与运行指南.md
```

## 验证命令

后端测试：

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python -m pytest
```

前端构建：

```powershell
cd frontend
npm run build
```

前端 lint：

```powershell
cd frontend
npm run lint
```

当前本地验证结果：

```text
后端测试：35 passed
前端构建：通过
前端 lint：通过
```

## 演示流程

推荐按以下流程演示：

1. 注册新用户
2. 登录系统
3. 发布帖子
4. 查看帖子详情
5. 发表评论
6. 点赞帖子
7. 进入个人中心
8. 查看我的帖子、我的评论和统计数据
9. 删除自己的帖子或评论
10. 修改密码并重新登录

## API 文档

后端启动后可以访问 FastAPI 自动文档：

```text
http://127.0.0.1:8000/docs
```

项目内 API 说明文档：

```text
docs/API_REFERENCE.md
```

## 后续扩展方向

- 接入 DeepSeek API 或 OpenAI Compatible API
- 实现 AI 回复帖子
- 实现 AI 情绪分析
- 增加 AI 标签和热点总结
- 增加举报系统
- 增加管理员后台
- 增加 Nginx + Systemd 部署配置
- 部署到公网服务器

## 说明

当前版本适合作为课程设计 MVP、本地演示和答辩说明项目。如果需要作为正式上线项目，还需要继续补充 AI 模块、生产部署、安全配置和更多异常场景测试。
