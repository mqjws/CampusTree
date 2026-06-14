# CampusTree —— 校园树洞匿名交流平台

## 项目简介

CampusTree 是一款面向大学生群体的匿名树洞交流平台。

用户可以在平台中：

- 匿名发布校园生活、学习心得和情绪倾诉
- 浏览树洞帖子
- 评论帖子
- 点赞帖子
- 使用 AI 助手获取回复和情绪分析
- 查看校园热门话题

本项目采用前后端分离架构，当前目标是完成课程设计答辩所需的 MVP 版本。

---

## 技术栈

### Frontend

- Vue3
- Vite
- TypeScript
- Element Plus
- Pinia
- Axios
- Vue Router

### Backend

- Python 3.11+
- FastAPI
- SQLModel
- Alembic
- JWT Authentication
- Uvicorn

### Database

- PostgreSQL 16

### AI

- DeepSeek API
- OpenAI Compatible API

### Deployment

- Ubuntu 24.04
- Nginx
- Systemd

---

## 系统架构

```text
Browser
  ↓
Vue3 + Vite + TypeScript Frontend
  ↓
REST API
  ↓
FastAPI Backend
  ↓
SQLModel
  ↓
PostgreSQL 16

FastAPI Backend
  ↓
DeepSeek API / OpenAI Compatible API
```

---

## 功能规划

### V1.0 核心版

用户系统：

- 注册
- 登录
- JWT 认证
- 修改密码
- 修改头像

帖子系统：

- 发布帖子
- 浏览帖子
- 查看帖子详情
- 删除帖子
- 搜索帖子
- 分页查询帖子

评论系统：

- 发布评论
- 删除评论
- 查看评论
- 分页查询评论

点赞系统：

- 点赞帖子
- 取消点赞
- 查询点赞数量

### V2.0 AI 版

AI 助手：

- AI 回复帖子
- AI 情绪分析
- AI 生成标签
- AI 热点总结

### V3.0 扩展版

后续可扩展：

- 实时聊天
- Windows 客户端
- Android 客户端
- 管理员后台
- 举报系统
- 数据统计看板

---

## 数据库设计方向

数据库使用 PostgreSQL 16。

核心表建议：

- `users`
- `posts`
- `comments`
- `post_likes`
- `ai_logs` 或 `ai_results`

通用字段：

- `id`
- `created_at`
- `updated_at`

数据库结构变更统一使用 Alembic 管理。

---

## API 设计方向

接口统一以 `/api/v1` 作为前缀。

用户接口：

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/users/me`
- `PUT /api/v1/users/me`

帖子接口：

- `POST /api/v1/posts`
- `GET /api/v1/posts`
- `GET /api/v1/posts/{post_id}`
- `DELETE /api/v1/posts/{post_id}`

评论接口：

- `POST /api/v1/comments`
- `GET /api/v1/posts/{post_id}/comments`
- `DELETE /api/v1/comments/{comment_id}`

点赞接口：

- `POST /api/v1/posts/{post_id}/like`
- `DELETE /api/v1/posts/{post_id}/like`

AI 接口：

- `POST /api/v1/ai/reply`
- `POST /api/v1/ai/analyze`

---

## 项目目录建议

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
│   ├── PROJECT_CONTEXT.md
│   ├── PROMPTS.md
│   ├── expand.md
│   └── result.md
└── README.md
```

---

## 开发原则

- 先设计，再实现
- 不一次性生成整个项目
- 每次只完成一个清晰模块
- 后端业务逻辑放在 `services`
- API 请求和响应结构使用明确类型
- 数据库变更通过 Alembic 迁移
- 前端使用 TypeScript 管理类型
- AI 能力由后端统一封装

---

## 开发计划

第一阶段：

- 设计 PostgreSQL 数据表
- 搭建 FastAPI 项目结构
- 配置 SQLModel 和 Alembic

第二阶段：

- 实现用户注册
- 实现用户登录
- 实现 JWT 认证

第三阶段：

- 实现帖子发布
- 实现帖子列表
- 实现帖子详情
- 实现帖子删除和搜索

第四阶段：

- 实现评论模块
- 实现点赞模块

第五阶段：

- 接入 DeepSeek API
- 实现 AI 回复帖子
- 实现 AI 情绪分析

第六阶段：

- 搭建 Vue3 + Vite + TypeScript 前端
- 完成前后端联调

第七阶段：

- 使用 Nginx + Systemd 部署到 Ubuntu 24.04

---

## 答辩亮点

1. 前后端分离架构
2. FastAPI 自动生成接口文档
3. JWT 身份认证
4. PostgreSQL 数据库设计
5. Alembic 数据库迁移
6. AI 能力集成
7. Nginx + Systemd 公网部署
8. 保留 Windows 客户端和 Android 客户端扩展空间

---

## 项目最终目标

实现一个能够实际运行、可公网访问、具备 AI 互动能力的校园树洞交流平台。
