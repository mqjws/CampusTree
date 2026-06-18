# CampusTree Frontend Project Bootstrap

## 1. 目标

本文档用于记录 CampusTree 前端第一阶段基础设施初始化过程。本阶段只完成项目基础设施，不开发业务页面，不开发业务组件。

本阶段范围：

1. 初始化项目
2. 安装依赖
3. 创建目录结构
4. 配置 Router
5. 配置 Pinia
6. 配置 Axios
7. 配置 Element Plus
8. 配置 ESLint 和 Prettier

---

## 2. 执行命令

### 2.1 初始化项目

```bash
npm create vite@latest frontend -- --template vue-ts
```

目的：
- 创建 Vue 3 + TypeScript 的 Vite 项目骨架
- 建立后续 Router、Pinia、Axios、Element Plus 的接入基础

### 2.2 安装基础依赖

```bash
cd frontend
npm install
```

目的：
- 安装脚手架默认依赖
- 确保项目可以进行本地启动和构建

### 2.3 安装运行时依赖

```bash
npm install vue-router pinia axios element-plus @element-plus/icons-vue
```

目的：
- `vue-router`：页面路由管理
- `pinia`：全局状态管理
- `axios`：HTTP 请求封装
- `element-plus`：基础 UI 组件库
- `@element-plus/icons-vue`：Element Plus 图标支持

### 2.4 安装代码规范依赖

```bash
npm install -D eslint prettier @eslint/js typescript-eslint eslint-plugin-vue eslint-config-prettier eslint-plugin-prettier @vue/eslint-config-typescript
```

目的：
- 建立 TypeScript + Vue 的静态检查能力
- 建立格式化规范，降低协作成本
- 避免 ESLint 与 Prettier 规则冲突

---

## 3. 创建顺序

### Step 1. 初始化 Vite 项目
- 先生成 Vue3 + TypeScript 基础工程
- 不直接手写底层配置，优先复用标准脚手架

### Step 2. 安装项目依赖
- 先装默认依赖，再补 Router / Pinia / Axios / Element Plus
- 最后安装 ESLint / Prettier 相关开发依赖

### Step 3. 调整入口文件
- 替换默认示例代码
- 将应用入口切换为 App + Router + Pinia + Element Plus

### Step 4. 创建目录骨架
- 先建立基础目录
- 再补充 router、stores、api、plugins、styles 等基础设施文件

### Step 5. 配置工程能力
- 配置路径别名
- 配置环境变量
- 配置 lint / format 脚本

### Step 6. 验证项目可运行
- 执行 lint
- 执行 build
- 确认在没有业务页面的前提下项目仍可正常构建

---

## 4. 当前文件结构

```text
frontend/
├─ public/
├─ src/
│  ├─ api/
│  │  └─ request.ts
│  ├─ assets/
│  │  └─ styles/
│  │     ├─ global.css
│  │     ├─ reset.css
│  │     └─ variables.css
│  ├─ plugins/
│  │  └─ element-plus.ts
│  ├─ router/
│  │  ├─ guards.ts
│  │  ├─ index.ts
│  │  └─ routes.ts
│  ├─ stores/
│  │  ├─ index.ts
│  │  └─ modules/
│  │     └─ auth.ts
│  ├─ views/
│  │  └─ system/
│  │     └─ SystemPlaceholderView.vue
│  ├─ App.vue
│  ├─ env.d.ts
│  └─ main.ts
├─ .env.development
├─ .env.production
├─ .eslintignore
├─ .prettierignore
├─ .prettierrc.json
├─ eslint.config.js
├─ index.html
├─ package.json
├─ tsconfig.app.json
└─ vite.config.ts
```

---

## 5. 每一步目的

### 5.1 初始化项目
- 建立标准 Vue 3 工程入口
- 避免从零拼装构建链路

### 5.2 安装依赖
- 补齐路由、状态、请求、UI 库能力
- 为后续业务模块开发提供基础

### 5.3 创建目录结构
- 提前约束代码组织方式
- 保持与 `FRONTEND_ARCHITECTURE.md` 一致

### 5.4 配置 Router
- 提前落好页面导航和路由守卫骨架
- 当前只提供系统占位视图，不进入业务实现

### 5.5 配置 Pinia
- 建立统一状态入口
- 当前仅保留 `auth` 基础状态作为认证流骨架

### 5.6 配置 Axios
- 建立统一请求实例
- 提前处理 `baseURL`、超时、Token 注入、401 清理逻辑

### 5.7 配置 Element Plus
- 建立全局 UI 库接入能力
- 后续业务页面和通用组件可直接使用

### 5.8 配置 ESLint 和 Prettier
- 在项目早期统一代码风格
- 减少后续多人协作时的格式噪音

---

## 6. 本阶段完成结果

本阶段完成后，项目应具备以下能力：

- 能运行 Vue3 + TypeScript + Vite 项目
- 已接入 Router
- 已接入 Pinia
- 已接入 Axios
- 已接入 Element Plus
- 已完成全局样式基础令牌
- 已完成 ESLint / Prettier 基础配置
- 已具备后续业务开发的目录骨架

明确不包含：

- 业务页面开发
- 业务组件开发
- API 业务模块开发
- 真实登录逻辑
- 真实帖子、评论、用户中心页面

---

## 7. 下一步建议

第二阶段建议开始以下工作：

1. 搭建 `AppLayout` 基础布局
2. 实现认证页面壳层
3. 实现首页、帖子详情、发布页、个人中心的空页面结构
4. 建立 API 模块分层文件
5. 增加 `uiStore`、`postStore`、`commentStore`、`userStore` 骨架
