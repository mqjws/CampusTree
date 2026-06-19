# CampusTree 项目技术上下文文档

## 项目名称

CampusTree

校园树洞匿名交流平台

---

## 项目目标

CampusTree 是一套面向大学生的匿名树洞交流平台。

项目要求：

- 前后端分离
- 支持公网部署
- 支持 AI 功能扩展
- 保留未来 Windows 客户端扩展空间
- 保留未来 Android 客户端扩展空间

当前目标：

完成课程设计答辩，交付一套可运行、可部署、可演示、可讲解的 MVP 项目。

---

## 技术栈迁移说明

项目已从原 Java 技术栈迁移为 Python FastAPI 技术栈。

旧技术栈：

- Java 21
- Spring Boot 3
- MyBatis Plus
- MySQL

新技术栈：

- Vue3 + Vite + TypeScript
- FastAPI + SQLModel + Alembic
- PostgreSQL 16
- JWT Authentication
- DeepSeek API / OpenAI Compatible API

功能范围保持不变：

- 用户系统
- 帖子系统
- 评论系统
- 点赞系统
- AI 助手

---

## 开发模式

本项目采用 AI Assisted Development，也就是 AI 辅助开发方式。

所有代码应满足：

- 易理解
- 易维护
- 易扩展
- 适合大学生阅读和答辩
- 模块划分清晰
- 避免不必要的复杂抽象

禁止：

- 过度设计
- 微服务
- 分布式架构
- 复杂中间件
- 一次性生成大量不可控代码

---

## 技术栈

### 前端

- Vue3
- Vite
- TypeScript
- Element Plus
- Pinia
- Axios
- Vue Router

前端职责：

- 页面展示
- 表单交互
- 用户状态管理
- 调用后端 REST API
- 展示帖子、评论、点赞和 AI 返回结果

### 后端

- Python 3.11+
- FastAPI
- SQLModel
- Alembic
- JWT Authentication
- Uvicorn

后端职责：

- 用户注册和登录
- JWT 签发与认证
- 帖子、评论、点赞业务逻辑
- AI 接口封装
- 数据库访问
- 统一 API 响应

### 数据库

- PostgreSQL 16

数据库职责：

- 存储用户信息
- 存储帖子内容
- 存储评论内容
- 存储点赞关系
- 存储 AI 分析结果或 AI 调用记录

### AI 能力

- DeepSeek API
- OpenAI Compatible API

AI 功能：

- AI 回复帖子
- AI 情绪分析
- 后续可扩展 AI 标签生成、AI 热点总结、AI 关键词提取

### 部署环境

- Ubuntu 24.04
- Nginx
- Systemd
- PostgreSQL 16

部署方式：

- 前端使用 Vite 构建静态文件，由 Nginx 托管
- 后端使用 Uvicorn 运行 FastAPI
- 使用 Systemd 管理后端服务
- Nginx 反向代理后端 API

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

## MVP 阶段功能

当前只开发以下功能。

### 用户系统

功能：

- 注册
- 登录
- JWT 认证
- 获取当前用户信息
- 修改密码
- 修改头像

### 帖子系统

功能：

- 发布帖子
- 浏览帖子
- 查看帖子详情
- 删除帖子
- 搜索帖子
- 分页查询帖子

### 评论系统

功能：

- 发布评论
- 删除评论
- 查看评论
- 分页查询评论

### 点赞系统

功能：

- 点赞帖子
- 取消点赞
- 查询帖子点赞数量
- 判断当前用户是否已点赞

### AI 助手

功能：

- AI 回复帖子
- AI 情绪分析

调用：

- DeepSeek API
- OpenAI Compatible API

---

## 非当前阶段功能

以下功能不在当前 MVP 阶段开发：

- Windows 客户端
- Android 客户端
- 实时聊天
- WebSocket
- Redis
- Docker 集群
- 支付系统
- 会员系统
- 人脸识别

这些功能可作为后续迭代方向。

---

## 项目目录规范

建议目录结构：

```text
CampusTree
├── backend
│   ├── app
│   │   ├── api
│   │   │   ├── deps.py
│   │   │   └── v1
│   │   │       ├── auth.py
│   │   │       ├── users.py
│   │   │       ├── posts.py
│   │   │       ├── comments.py
│   │   │       ├── likes.py
│   │   │       └── ai.py
│   │   ├── core
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── response.py
│   │   ├── db
│   │   │   ├── session.py
│   │   │   └── init_db.py
│   │   ├── models
│   │   │   ├── user.py
│   │   │   ├── post.py
│   │   │   ├── comment.py
│   │   │   └── like.py
│   │   ├── schemas
│   │   │   ├── user.py
│   │   │   ├── post.py
│   │   │   ├── comment.py
│   │   │   └── ai.py
│   │   ├── services
│   │   │   ├── user_service.py
│   │   │   ├── post_service.py
│   │   │   ├── comment_service.py
│   │   │   ├── like_service.py
│   │   │   └── ai_service.py
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
│   │   ├── views
│   │   ├── App.vue
│   │   └── main.ts
│   ├── index.html
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

## API 规范

统一返回格式：

```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

错误返回格式：

```json
{
  "code": 500,
  "message": "error",
  "data": null
}
```

分页返回建议：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [],
    "total": 0,
    "page": 1,
    "page_size": 10
  }
}
```

接口路径建议统一使用：

```text
/api/v1
```

---

## 数据库规范

数据库使用 PostgreSQL 16。

命名规范：

- 表名使用小写加下划线，例如 `users`、`posts`、`post_likes`
- 字段名使用小写加下划线，例如 `created_at`、`updated_at`
- 主键统一使用 `id`
- 外键字段使用 `{entity}_id`，例如 `user_id`、`post_id`

通用字段：

- `id`
- `created_at`
- `updated_at`

字段类型建议：

- 主键：`BIGSERIAL` 或 SQLModel 自动生成整数主键
- 短文本：`VARCHAR`
- 长文本：`TEXT`
- 时间：`TIMESTAMP WITH TIME ZONE`
- 布尔值：`BOOLEAN`
- 计数字段：`INTEGER`

迁移规范：

- 使用 Alembic 管理数据库结构变更
- 禁止直接手动修改生产数据库结构
- 每次模型结构变化都应生成迁移文件
- 迁移文件需要能正向升级和回滚

核心表建议：

- `users`
- `posts`
- `comments`
- `post_likes`
- `ai_logs` 或 `ai_results`

---

## 编码规范

### Python 后端

- 使用 Python 3.11+
- 使用类型标注
- 使用 Pydantic / SQLModel 定义数据结构
- API 层只处理请求和响应
- 业务逻辑放在 `services`
- 数据模型放在 `models`
- 请求和响应结构放在 `schemas`
- 配置统一放在 `core/config.py`
- JWT、密码加密等安全逻辑放在 `core/security.py`
- 避免在路由函数中堆叠复杂业务代码

### TypeScript 前端

- 使用 TypeScript
- API 请求统一放在 `src/api`
- 页面放在 `src/views`
- 通用组件放在 `src/components`
- 状态管理放在 `src/stores`
- 类型定义放在 `src/types`
- 路由配置放在 `src/router`
- 避免在页面组件中直接写大量请求逻辑

### 命名规范

后端：

- 文件名使用小写加下划线
- Python 变量和函数使用 `snake_case`
- 类名使用 `PascalCase`
- API 路由文件按业务模块命名

前端：

- Vue 组件使用 `PascalCase`
- TypeScript 变量和函数使用 `camelCase`
- 类型和接口使用 `PascalCase`

---

## AI 开发规范

AI 模块必须通过后端统一封装，前端不得直接调用 DeepSeek API。

要求：

- API Key 只允许保存在后端环境变量中
- 不允许提交真实 API Key
- 提供 `.env.example`
- AI 返回内容需要做异常处理
- AI 功能失败时不能影响核心发帖、评论、点赞流程
- AI 输出不能作为医疗诊断，只能作为情绪陪伴和学习建议

AI 功能开发流程：

1. 明确使用场景
2. 设计请求和响应结构
3. 设计数据库是否需要保存 AI 结果
4. 封装后端 AI 服务
5. 提供 API 接口
6. 前端展示 AI 结果
7. 增加错误提示和超时处理

---

## 项目最终目标

完成一套：

- 可运行
- 可部署
- 可答辩
- 可演示
- 支持 AI 扩展

的校园树洞平台。
