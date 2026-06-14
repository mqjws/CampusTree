# CampusTree 项目内容说明

## 1. 项目概述

CampusTree 是一个面向大学生的校园树洞匿名交流平台。项目目标是完成一套可运行、可部署、可答辩、可演示的课程设计项目。

平台核心定位是：让学生可以匿名发布树洞帖子、浏览帖子、评论互动、点赞，并接入 AI 能力，例如 AI 回复和情绪分析。

## 2. 技术栈迁移结果

项目已从原 Java 后端方案迁移为 Python FastAPI 后端方案。

旧方案：

- Java 21
- Spring Boot 3
- MyBatis Plus
- MySQL

新方案：

- 前端：Vue3、Vite、TypeScript、Element Plus、Pinia、Axios
- 后端：Python 3.11+、FastAPI、SQLModel、Alembic、JWT Authentication
- 数据库：PostgreSQL 16
- AI：DeepSeek API、OpenAI Compatible API
- 部署：Ubuntu 24.04、Nginx、Systemd

## 3. 当前项目状态

当前项目仍处于文档和规划阶段，暂未发现实际前端或后端业务代码。

现有目录结构：

```text
CampusTree
├── backend
├── frontend
├── docs
│   ├── PROJECT_CONTEXT.md
│   ├── PROMPTS.md
│   ├── expand.md
│   └── result.md
└── README.md
```

其中：

- `backend`：后端目录，目前为空，后续用于 FastAPI 项目。
- `frontend`：前端目录，目前为空，后续用于 Vue3 + Vite + TypeScript 项目。
- `docs/PROJECT_CONTEXT.md`：项目技术上下文文档。
- `docs/PROMPTS.md`：后续 AI 分阶段开发提示词。
- `docs/expand.md`：课程设计加分项和扩展功能建议。
- `docs/result.md`：当前项目内容说明文档。
- `README.md`：项目总览文档。

## 4. MVP 功能范围

当前项目保持原功能目标不变。

### 用户系统

- 注册
- 登录
- JWT 认证
- 修改密码
- 修改头像

### 帖子系统

- 发布帖子
- 浏览帖子
- 查看帖子详情
- 删除帖子
- 搜索帖子
- 分页查询帖子

### 评论系统

- 发布评论
- 删除评论
- 查看评论
- 分页查询评论

### 点赞系统

- 点赞帖子
- 取消点赞
- 查询点赞数量
- 判断当前用户是否已点赞

### AI 助手

- AI 回复帖子
- AI 情绪分析

## 5. 新系统架构

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

## 6. 新目录结构建议

```text
CampusTree
├── backend
│   ├── app
│   │   ├── api
│   │   │   └── v1
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

## 7. 数据库规范

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

表名和字段名统一使用小写加下划线。

数据库结构变更统一使用 Alembic 管理。

## 8. 开发原则

- 先设计，再实现
- 不一次性生成整个项目
- 每次只完成一个模块
- API 层只处理请求和响应
- 业务逻辑放在 `services`
- 数据模型放在 `models`
- 请求和响应结构放在 `schemas`
- 数据库变更通过 Alembic 管理
- 前端使用 TypeScript 管理类型
- AI 能力只通过后端封装调用

## 9. 推荐开发顺序

1. PostgreSQL 数据库设计
2. FastAPI 后端基础结构
3. SQLModel 和 Alembic 配置
4. 用户注册、登录、JWT 认证
5. Vue3 + Vite + TypeScript 前端基础结构
6. 帖子模块
7. 评论模块
8. 点赞模块
9. AI 模块
10. Nginx + Systemd 部署

## 10. 下一步建议

下一阶段建议先完成“用户系统数据库设计”，包括：

- `users` 表 SQL
- 用户字段说明
- 密码加密和 JWT 认证说明
- 用户注册和登录 API 设计
- Alembic 迁移策略

完成数据库设计后，再搭建 FastAPI 项目基础结构。
