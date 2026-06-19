# CampusTree 当前项目状态

更新时间：2026-06-19

## 总体判断

CampusTree 当前已经可以作为课程设计的本地 MVP 演示项目使用。

但还不能称为完整的生产级最终版本，因为 AI 功能和真实生产部署还没有完成。

## 当前分支情况

本地当前分支：

```text
frontend-dev
```

本地检测到的远端分支：

```text
origin/main
origin/frontend-dev
```

当前情况：

- `main` 分支目前主要是完整后端实现。
- `frontend-dev` 分支包含当前完整 MVP 版本，包括前端页面和前后端联调。
- 如果需要在本地运行完整项目，目前应该使用 `frontend-dev` 分支。

建议的最终仓库结构：

- 在最终提交或分享前，将 `frontend-dev` 合并到 `main`。
- 让 `main` 成为唯一的稳定可运行分支。
- 如果暂时不合并，需要切换到 `frontend-dev` 分支。

## 已完成的 MVP 功能

### 后端

- FastAPI 应用结构。
- 通过 SQLModel 连接 PostgreSQL。
- Alembic 数据库迁移。
- 用户注册。
- 用户登录。
- JWT 身份认证。
- 获取当前登录用户。
- 查询当前用户发布的帖子。
- 查询当前用户发表的评论。
- 查询当前用户统计数据。
- 修改密码。
- 帖子创建、列表、详情、修改、删除。
- 评论创建、列表、详情、修改、删除。
- 帖子点赞和取消点赞。
- 业务接口统一成功和错误响应格式。
- 已配置本地前端开发所需的 CORS。

### 前端

- Vue 3 + Vite + TypeScript 项目结构。
- Element Plus UI 组件库集成。
- Pinia 状态管理。
- Axios 请求封装，并自动携带 token。
- Vue Router 路由和登录守卫。
- 登录页面。
- 注册页面。
- 首页帖子列表。
- 帖子详情页。
- 发布帖子页。
- 评论展示和发布。
- 点赞和取消点赞接口接入。
- 用户个人中心。
- 我的帖子列表。
- 我的评论列表。
- 删除自己的帖子。
- 删除自己的评论。
- 设置页支持修改密码和退出登录。

### 文档

- API 文档位于 `docs/API_REFERENCE.md`。
- 已有前端架构、UI 规划等设计文档。
- 当前文档用于记录最新 MVP 状态。

## 本地验证结果

以下检查已在 2026-06-19 本地通过。

后端测试：

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest
```

结果：

```text
35 passed
```

前端构建：

```powershell
cd frontend
npm run build
```

结果：

```text
构建成功
```

前端代码检查：

```powershell
cd frontend
npm run lint
```

结果：

```text
检查通过，无报错
```

构建时存在的提示：

- Vite/Rolldown 对依赖中的 pure annotation 有警告。
- 前端打包后存在 chunk 体积偏大的警告。

这些警告不影响课程设计 MVP 的本地演示。

## 尚未完成的内容

### AI 模块

README 和规划文档中提到过：

- DeepSeek API。
- AI 回复帖子。
- AI 情绪分析。
- AI 标签生成。
- AI 总结。

当前代码中还没有实现这些功能。

如果用于课程设计演示，可以把 AI 模块说明为后续扩展功能。

### 生产部署

项目目前还没有最终生产部署文件，例如：

- Nginx 站点配置。
- Systemd 后端服务配置。
- 自动化部署脚本。
- 已验证可访问的公网域名部署。

当前前端生产环境变量中有：

```text
https://api.campustree.com/api/v1
```

如果后续真正部署，而这个域名不可用，需要修改为实际后端 API 地址。

## 当前 Git 工作区状态

生成本文档时，本地还有未提交改动，主要包括：

- 后端 CORS 配置。
- 前端删除帖子 API。
- 前端删除评论 API。
- 个人中心删除帖子和评论操作。
- 相关 store 和类型定义。
- 当前项目状态文档。
- 本地运行部署指南。

在提交 GitHub 前，建议先 commit 并 push。

## 最终建议

如果用于课程设计：

```text
当前项目已经达到本地 MVP 演示标准。
```

如果用于 GitHub 最终交付：

```text
建议将 frontend-dev 合并到 main，然后直接克隆 main 分支。
```

如果暂时不合并：

```text
需要 checkout frontend-dev，因为 main 目前只有后端。
```
