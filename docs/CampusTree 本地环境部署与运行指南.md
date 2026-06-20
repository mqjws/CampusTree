# CampusTree 本地环境部署与运行指南

本文档用于指导从 GitHub 拉取项目后，在本地运行 CampusTree。

## 1. 应该使用哪个分支

需要使用同时包含后端和前端的分支。

当前推荐分支：

```text
main
```

克隆并切换分支：

```powershell
git clone <你的 GitHub 仓库地址>
cd CampusTree
git checkout main
```

## 2. 需要提前安装的软件

请先安装以下软件：

- Git
- Python 3.11 或更高版本
- Node.js 20 或更高版本
- PostgreSQL 16

推荐安装(可选)：

- VS Code
- Postman 或 Apifox，用于测试接口

## 3. 创建 PostgreSQL 数据库

打开 PowerShell 或 PostgreSQL 命令行，创建数据库：

```powershell
createdb -U postgres -h 127.0.0.1 -p 5432 campustree
```

如果 PowerShell 中无法使用 `createdb` 命令，也可以使用 pgAdmin 或 PostgreSQL shell 手动创建数据库。

数据库名称为：

```text
campustree
```

## 4. 后端环境配置

进入后端目录：

```powershell
cd backend
```

创建 Python 虚拟环境：

```powershell
python -m venv .venv
```

激活虚拟环境：

```powershell
.\.venv\Scripts\Activate.ps1
```

如果 PowerShell 提示禁止运行脚本，可以在当前 PowerShell 窗口执行：

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

然后再次激活虚拟环境：

```powershell
.\.venv\Scripts\Activate.ps1
```

安装后端依赖：

```powershell
pip install -r requirements.txt
```

复制环境变量文件：

```powershell
Copy-Item .env.example .env
```

打开 `backend/.env`，修改数据库连接中的密码：

```text
DATABASE_URL=postgresql+psycopg://postgres:your_password@127.0.0.1:5432/campustree
```

将 `your_password` 替换为自己电脑上 PostgreSQL 的 `postgres` 用户密码。

同时设置 JWT 密钥：

```text
JWT_SECRET_KEY=replace_with_a_long_random_secret
```

可以临时改成类似下面的内容：

```text
JWT_SECRET_KEY=campustree_local_dev_secret_please_change
```

执行数据库迁移：

```powershell
alembic upgrade head
```

启动后端服务：

```powershell
uvicorn app.main:app --reload
```

后端访问地址：

```text
http://127.0.0.1:8000
```

接口文档地址：

```text
http://127.0.0.1:8000/docs
```

## 5. 前端环境配置

重新打开一个 PowerShell 窗口。

进入前端目录：

```powershell
cd frontend
```

安装前端依赖：

```powershell
npm install
```

检查本地前端环境变量文件：

```text
frontend/.env.development
```

内容应为：

```text
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_TITLE=CampusTree
```

启动前端开发服务器：

```powershell
npm run dev
```

前端默认访问地址通常是：

```text
http://localhost:5173
```

在浏览器中打开即可。

## 6. 每次本地运行的启动顺序

每次本地运行项目时，按以下顺序操作。

第一步，启动 PostgreSQL。

第二步，启动后端：

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

第三步，另开一个终端启动前端：

```powershell
cd frontend
npm run dev
```

第四步，浏览器打开：

```text
http://localhost:5173
```

## 7. 基础演示流程

可以按照下面流程验证项目是否运行正常：

1. 注册一个新用户。
2. 登录系统。
3. 发布一条帖子。
4. 进入帖子详情页。
5. 发表评论。
6. 点赞帖子。
7. 进入个人中心。
8. 查看我的帖子、我的评论和统计数据。
9. 尝试删除自己发布的帖子或评论。
10. 在设置页修改密码。

## 8. 运行检查命令

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

前端代码检查：

```powershell
cd frontend
npm run lint
```

## 9. 常见问题

### 后端无法连接数据库

请检查：

- PostgreSQL 是否已经启动。
- 是否已经创建 `campustree` 数据库。
- `backend/.env` 中的数据库密码是否正确。
- `DATABASE_URL` 中的端口是否为 `5432`。

### 提示找不到 alembic 命令

请确认已经激活后端虚拟环境：

```powershell
.\.venv\Scripts\Activate.ps1
```

然后重新安装依赖：

```powershell
pip install -r requirements.txt
```

### 前端无法访问后端接口

请检查：

- 后端是否运行在 `http://127.0.0.1:8000`。
- `frontend/.env.development` 是否指向 `http://localhost:8000/api/v1`。
- 浏览器控制台是否存在 CORS 报错。

### 登录后突然退出

当前前端在后端返回 `401` 时会删除本地 token。

遇到这种情况，重新登录即可。

## 10. 关于 AI 和部署的说明

当前 MVP 版本还没有实现 AI 功能。

当前 MVP 主要用于本地演示。如果要部署到公网，还需要额外配置 Nginx、Systemd 和真实域名。
