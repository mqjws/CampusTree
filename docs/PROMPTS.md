# PROMPTS.md

本文件用于指导 AI 分阶段开发 CampusTree 项目。

当前技术栈：

- Frontend：Vue3、Vite、TypeScript、Element Plus、Pinia、Axios
- Backend：Python 3.11+、FastAPI、SQLModel、Alembic、JWT Authentication
- Database：PostgreSQL 16
- AI：DeepSeek API、OpenAI Compatible API
- Deployment：Ubuntu 24.04、Nginx、Systemd

要求：

- 不要一次性生成整个项目
- 每次只完成一个模块
- 先设计，再实现
- 不生成未被要求的业务代码
- 文档、数据库、接口、代码要同步更新

---

## Prompt 1

你是一名资深 Python FastAPI 架构师。

请阅读 `docs/PROJECT_CONTEXT.md`。

严格遵守项目规范。

不要一次生成整个项目。

请先完成：

用户系统 PostgreSQL 数据库设计。

输出：

1. SQL 建表语句
2. SQLModel 模型设计说明
3. 字段说明
4. ER 关系说明
5. Alembic 迁移建议

---

## Prompt 2

请阅读 `docs/PROJECT_CONTEXT.md`。

基于用户系统数据库设计，实现 FastAPI 用户模块。

功能：

- 注册
- 登录
- JWT 认证
- 获取当前用户信息

输出：

1. 后端目录结构
2. 依赖配置
3. SQLModel 模型
4. 请求和响应 Schema
5. Service 层代码
6. API 路由代码
7. JWT 工具代码
8. 简单接口测试说明

---

## Prompt 3

请阅读 `docs/PROJECT_CONTEXT.md`。

实现帖子模块。

功能：

- 发帖
- 删除帖子
- 查询帖子详情
- 分页查询帖子
- 搜索帖子

输出：

1. PostgreSQL 数据库设计
2. SQLModel 模型
3. API 接口设计
4. FastAPI 后端代码
5. 前端调用建议

---

## Prompt 4

请阅读 `docs/PROJECT_CONTEXT.md`。

实现评论模块。

要求：

- 支持帖子评论
- 支持评论删除
- 支持评论分页
- 评论必须关联用户和帖子

输出：

1. 数据库设计
2. SQLModel 模型
3. API 接口设计
4. FastAPI 后端代码
5. 测试说明

---

## Prompt 5

请阅读 `docs/PROJECT_CONTEXT.md`。

实现点赞模块。

要求：

- 支持点赞帖子
- 支持取消点赞
- 同一用户不能重复点赞同一帖子
- 支持查询帖子点赞数量

输出：

1. PostgreSQL 表设计
2. 唯一约束设计
3. SQLModel 模型
4. FastAPI 接口代码
5. 并发和重复点赞处理说明

---

## Prompt 6

请阅读 `docs/PROJECT_CONTEXT.md`。

实现 AI 模块。

要求：

- 接入 DeepSeek API
- 使用 OpenAI Compatible API 调用方式
- 支持 AI 回复帖子
- 支持 AI 情绪分析
- API Key 只能从环境变量读取
- 前端不得直接调用 AI 服务

输出：

1. 后端 AI Service 设计
2. 配置文件说明
3. FastAPI 接口代码
4. 错误处理说明
5. 接口文档
6. 安全注意事项

---

## Prompt 7

请阅读 `docs/PROJECT_CONTEXT.md`。

搭建 Vue3 + Vite + TypeScript 前端基础结构。

要求：

- 使用 Element Plus
- 使用 Pinia
- 使用 Vue Router
- 使用 Axios 统一封装请求
- 支持 JWT Token 保存和请求拦截

输出：

1. 前端目录结构
2. 依赖配置
3. 路由设计
4. API 封装
5. Pinia 用户状态设计
6. 基础页面列表

---

## Prompt 8

请阅读 `docs/PROJECT_CONTEXT.md`。

设计 Ubuntu 24.04 部署方案。

要求：

- 前端由 Nginx 托管
- 后端由 Uvicorn 运行
- 后端服务由 Systemd 管理
- Nginx 反向代理 `/api`
- PostgreSQL 16 作为数据库

输出：

1. 部署目录建议
2. Nginx 配置示例
3. Systemd 服务配置示例
4. 环境变量配置说明
5. 部署流程
6. 常见问题排查
