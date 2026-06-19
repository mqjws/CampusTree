# CampusTree 前端架构设计

## 1. 项目目录结构

```
frontend/
├── public/
│   ├── favicon.ico
│   └── index.html
├── src/
│   ├── assets/              # 静态资源
│   │   ├── images/          # 图片资源
│   │   ├── icons/           # SVG图标
│   │   └── styles/          # 全局样式
│   │       ├── variables.css    # CSS变量（颜色、间距等）
│   │       ├── reset.css        # 样式重置
│   │       └── global.css       # 全局样式
│   │
│   ├── components/          # 通用组件
│   │   ├── layout/          # 布局组件
│   │   │   ├── AppHeader.vue        # 顶部导航栏
│   │   │   ├── AppFooter.vue        # 底部导航（移动端）
│   │   │   ├── AppLayout.vue        # 页面布局容器
│   │   │   └── AppSidebar.vue       # 侧边栏（预留）
│   │   │
│   │   ├── post/            # 帖子相关组件
│   │   │   ├── PostCard.vue         # 帖子卡片
│   │   │   ├── PostList.vue         # 帖子列表
│   │   │   ├── PostForm.vue         # 帖子表单
│   │   │   └── PostMeta.vue         # 帖子元信息（时间、点赞、评论数）
│   │   │
│   │   ├── comment/         # 评论相关组件
│   │   │   ├── CommentList.vue      # 评论列表
│   │   │   ├── CommentItem.vue      # 单条评论
│   │   │   └── CommentForm.vue      # 评论输入框
│   │   │
│   │   ├── user/            # 用户相关组件
│   │   │   ├── UserAvatar.vue       # 匿名头像
│   │   │   ├── UserInfoCard.vue     # 用户信息卡片
│   │   │   └── UserStats.vue        # 用户统计信息
│   │   │
│   │   └── common/          # 通用UI组件
│   │       ├── LoadingSpinner.vue   # 加载动画
│   │       ├── EmptyState.vue       # 空状态提示
│   │       ├── ErrorMessage.vue     # 错误提示
│   │       ├── LikeButton.vue       # 点赞按钮
│   │       └── InfiniteScroll.vue   # 无限滚动
│   │
│   ├── views/               # 页面视图
│   │   ├── auth/            # 认证相关页面
│   │   │   ├── LoginView.vue
│   │   │   └── RegisterView.vue
│   │   │
│   │   ├── home/            # 首页
│   │   │   └── HomeView.vue
│   │   │
│   │   ├── post/            # 帖子相关页面
│   │   │   ├── PostDetailView.vue   # 帖子详情
│   │   │   └── CreatePostView.vue   # 创建帖子
│   │   │
│   │   ├── profile/         # 用户中心
│   │   │   ├── ProfileView.vue      # 用户中心首页
│   │   │   ├── MyPostsView.vue      # 我的帖子
│   │   │   ├── MyCommentsView.vue   # 我的评论
│   │   │   └── SettingsView.vue     # 设置
│   │   │
│   │   └── error/           # 错误页面
│   │       ├── NotFoundView.vue     # 404
│   │       └── ErrorView.vue        # 通用错误
│   │
│   ├── router/              # 路由配置
│   │   ├── index.ts         # 路由主文件
│   │   └── guards.ts        # 路由守卫
│   │
│   ├── stores/              # Pinia状态管理
│   │   ├── auth.ts          # 认证状态
│   │   ├── post.ts          # 帖子状态
│   │   ├── comment.ts       # 评论状态
│   │   ├── user.ts          # 用户状态
│   │   └── ui.ts            # UI状态（loading、toast等）
│   │
│   ├── api/                 # API接口封装
│   │   ├── request.ts       # Axios实例配置
│   │   ├── auth.ts          # 认证接口
│   │   ├── post.ts          # 帖子接口
│   │   ├── comment.ts       # 评论接口
│   │   ├── like.ts          # 点赞接口
│   │   └── user.ts          # 用户接口
│   │
│   ├── utils/               # 工具函数
│   │   ├── format.ts        # 格式化函数（时间、数字）
│   │   ├── validate.ts      # 表单验证
│   │   ├── storage.ts       # 本地存储封装
│   │   └── constants.ts     # 常量定义
│   │
│   ├── types/               # TypeScript类型定义
│   │   ├── api.d.ts         # API响应类型
│   │   ├── models.d.ts      # 数据模型类型
│   │   └── common.d.ts      # 通用类型
│   │
│   ├── composables/         # 组合式函数
│   │   ├── usePost.ts       # 帖子相关逻辑
│   │   ├── useComment.ts    # 评论相关逻辑
│   │   ├── useLike.ts       # 点赞相关逻辑
│   │   └── useInfiniteScroll.ts  # 无限滚动逻辑
│   │
│   ├── App.vue              # 根组件
│   └── main.ts              # 入口文件
│
├── .env.development         # 开发环境变量
├── .env.production          # 生产环境变量
├── vite.config.ts           # Vite配置
├── tsconfig.json            # TypeScript配置
└── package.json             # 依赖配置
```

### 目录职责说明

**assets/**：存放静态资源
- `images/`：图片文件（logo、默认头像等）
- `icons/`：SVG图标文件
- `styles/`：全局CSS样式，包括CSS变量、样式重置

**components/**：可复用的Vue组件
- 按功能模块划分（layout、post、comment、user、common）
- 组件名采用PascalCase命名
- 每个组件职责单一，便于维护和测试

**views/**：页面级组件
- 对应路由的页面组件
- 按功能模块划分子目录
- 页面组件负责组装业务逻辑和UI组件

**router/**：路由配置
- `index.ts`：定义所有路由规则
- `guards.ts`：路由守卫（权限控制、登录检查）

**stores/**：Pinia状态管理
- 按业务模块划分store
- 每个store负责一个领域的状态管理
- 使用组合式API风格

**api/**：API接口层
- `request.ts`：Axios实例、拦截器配置
- 其他文件按业务模块封装接口调用
- 统一处理请求/响应格式

**utils/**：工具函数库
- 纯函数，无副作用
- 可独立测试
- 按功能分类

**types/**：TypeScript类型定义
- 集中管理类型定义
- 提升代码可维护性和类型安全

**composables/**：Vue3组合式函数
- 封装可复用的业务逻辑
- 遵循use*命名约定

---

## 2. 页面清单

### 认证页面

| 页面名称 | 文件路径 | 路由路径 | 说明 |
|---------|---------|---------|------|
| 登录页 | `views/auth/LoginView.vue` | `/login` | 用户登录 |
| 注册页 | `views/auth/RegisterView.vue` | `/register` | 用户注册 |

### 核心业务页面

| 页面名称 | 文件路径 | 路由路径 | 说明 |
|---------|---------|---------|------|
| 首页 | `views/home/HomeView.vue` | `/` | 帖子列表流 |
| 帖子详情 | `views/post/PostDetailView.vue` | `/post/:id` | 查看帖子及评论 |
| 创建帖子 | `views/post/CreatePostView.vue` | `/create` | 发布新帖子 |

### 用户中心页面

| 页面名称 | 文件路径 | 路由路径 | 说明 |
|---------|---------|---------|------|
| 用户中心 | `views/profile/ProfileView.vue` | `/profile` | 用户中心首页 |
| 我的帖子 | `views/profile/MyPostsView.vue` | `/profile/posts` | 查看自己的帖子 |
| 我的评论 | `views/profile/MyCommentsView.vue` | `/profile/comments` | 查看自己的评论 |
| 设置 | `views/profile/SettingsView.vue` | `/profile/settings` | 账号设置 |

### 错误页面

| 页面名称 | 文件路径 | 路由路径 | 说明 |
|---------|---------|---------|------|
| 404页面 | `views/error/NotFoundView.vue` | `/:pathMatch(.*)` | 页面不存在 |
| 错误页面 | `views/error/ErrorView.vue` | `/error` | 通用错误页 |

---

## 3. Router设计

### 路由表结构

```typescript
// router/index.ts 路由配置概览

路由路径: /
├── /                          [首页] - 需要登录
├── /login                     [登录页] - 游客可访问
├── /register                  [注册页] - 游客可访问
│
├── /post/:id                  [帖子详情] - 需要登录
├── /create                    [发布帖子] - 需要登录
│
├── /profile                   [用户中心] - 需要登录
│   ├── /profile/posts         [我的帖子]
│   ├── /profile/comments      [我的评论]
│   └── /profile/settings      [设置]
│
├── /error                     [错误页]
└── /:pathMatch(.*)            [404页面]
```

### 路由配置详情

#### 公开路由（无需登录）

```typescript
// 登录页
{
  path: '/login',
  name: 'Login',
  component: () => import('@/views/auth/LoginView.vue'),
  meta: {
    requiresAuth: false,
    title: '登录 - CampusTree'
  }
}

// 注册页
{
  path: '/register',
  name: 'Register',
  component: () => import('@/views/auth/RegisterView.vue'),
  meta: {
    requiresAuth: false,
    title: '注册 - CampusTree'
  }
}
```

#### 受保护路由（需要登录）

```typescript
// 首页
{
  path: '/',
  name: 'Home',
  component: () => import('@/views/home/HomeView.vue'),
  meta: {
    requiresAuth: true,
    title: 'CampusTree - 校园匿名交流平台'
  }
}

// 帖子详情
{
  path: '/post/:id',
  name: 'PostDetail',
  component: () => import('@/views/post/PostDetailView.vue'),
  meta: {
    requiresAuth: true,
    title: '帖子详情'
  }
}

// 创建帖子
{
  path: '/create',
  name: 'CreatePost',
  component: () => import('@/views/post/CreatePostView.vue'),
  meta: {
    requiresAuth: true,
    title: '发布帖子'
  }
}

// 用户中心（嵌套路由）
{
  path: '/profile',
  component: () => import('@/views/profile/ProfileView.vue'),
  meta: { requiresAuth: true },
  children: [
    {
      path: '',
      name: 'Profile',
      component: () => import('@/views/profile/ProfileIndexView.vue'),
      meta: { title: '用户中心' }
    },
    {
      path: 'posts',
      name: 'MyPosts',
      component: () => import('@/views/profile/MyPostsView.vue'),
      meta: { title: '我的帖子' }
    },
    {
      path: 'comments',
      name: 'MyComments',
      component: () => import('@/views/profile/MyCommentsView.vue'),
      meta: { title: '我的评论' }
    },
    {
      path: 'settings',
      name: 'Settings',
      component: () => import('@/views/profile/SettingsView.vue'),
      meta: { title: '设置' }
    }
  ]
}
```

#### 错误路由

```typescript
// 错误页
{
  path: '/error',
  name: 'Error',
  component: () => import('@/views/error/ErrorView.vue'),
  meta: {
    requiresAuth: false,
    title: '出错了'
  }
}

// 404页面（放在最后）
{
  path: '/:pathMatch(.*)*',
  name: 'NotFound',
  component: () => import('@/views/error/NotFoundView.vue'),
  meta: {
    requiresAuth: false,
    title: '页面不存在'
  }
}
```

### 路由守卫（权限控制）

#### 全局前置守卫

**职责**：
1. 检查登录状态
2. 重定向未登录用户到登录页
3. 已登录用户访问登录页时重定向到首页
4. 更新页面标题

**逻辑流程**：

```typescript
// router/guards.ts

beforeEach 守卫逻辑：

1. 获取目标路由的 meta.requiresAuth
2. 从 authStore 获取登录状态

3. 如果需要登录 && 未登录：
   - 保存目标路径到 redirect 参数
   - 重定向到 /login?redirect=/target-path

4. 如果已登录 && 访问登录/注册页：
   - 重定向到首页 /

5. 更新页面标题：
   - document.title = route.meta.title

6. 允许导航
```

#### 路由守卫实现要点

**登录检查**：
- 检查 localStorage 中的 token
- 如果有 token，自动尝试获取用户信息
- 如果 token 失效，清除并跳转登录

**重定向处理**：
- 登录成功后跳转到之前的页面
- 使用 `query.redirect` 参数保存目标路径

**页面标题**：
- 动态更新 document.title
- 格式：`页面名 - CampusTree`

---

## 4. Pinia状态管理设计

### authStore（认证状态）

**文件**：`stores/auth.ts`

**职责**：管理用户认证状态、登录/注册/登出逻辑

#### State

```typescript
{
  token: string | null              // JWT token
  isAuthenticated: boolean          // 是否已登录
  user: User | null                 // 当前用户信息
  loading: boolean                  // 登录/注册加载状态
}
```

#### Getters

```typescript
{
  userId: (state) => state.user?.id           // 当前用户ID
  username: (state) => state.user?.username   // 用户名
  isLoggedIn: (state) => state.isAuthenticated && !!state.token
}
```

#### Actions

```typescript
{
  // 登录
  async login(username: string, password: string)
  
  // 注册
  async register(username: string, password: string)
  
  // 登出
  logout()
  
  // 从token恢复登录状态
  async restoreAuth()
  
  // 更新用户信息
  async fetchUserInfo()
  
  // 清除认证信息
  clearAuth()
}
```

**数据持久化**：
- token 存储在 localStorage
- 页面刷新时自动恢复登录状态

---

### postStore（帖子状态）

**文件**：`stores/post.ts`

**职责**：管理帖子列表、当前帖子详情、发布/删除帖子

#### State

```typescript
{
  posts: Post[]                     // 帖子列表
  currentPost: Post | null          // 当前查看的帖子详情
  
  pagination: {
    page: number                    // 当前页码
    pageSize: number                // 每页条数
    total: number                   // 总条数
    hasMore: boolean                // 是否还有更多
  }
  
  loading: boolean                  // 加载状态
  error: string | null              // 错误信息
}
```

#### Getters

```typescript
{
  // 获取帖子列表
  postList: (state) => state.posts
  
  // 根据ID获取帖子
  getPostById: (state) => (id: number) => 
    state.posts.find(p => p.id === id)
  
  // 是否正在加载
  isLoading: (state) => state.loading
}
```

#### Actions

```typescript
{
  // 获取帖子列表（分页）
  async fetchPosts(page: number = 1)
  
  // 加载更多帖子（无限滚动）
  async loadMorePosts()
  
  // 获取帖子详情
  async fetchPostDetail(id: number)
  
  // 创建帖子
  async createPost(data: CreatePostDto)
  
  // 删除帖子
  async deletePost(id: number)
  
  // 点赞/取消点赞帖子
  async toggleLike(id: number)
  
  // 清空帖子列表（用于刷新）
  clearPosts()
}
```

---

### commentStore（评论状态）

**文件**：`stores/comment.ts`

**职责**：管理帖子的评论列表、发表/删除评论

#### State

```typescript
{
  comments: Record<number, Comment[]>   // 按帖子ID索引的评论列表
  loading: boolean                      // 加载状态
  error: string | null                  // 错误信息
}
```

#### Getters

```typescript
{
  // 获取指定帖子的评论
  getCommentsByPostId: (state) => (postId: number) => 
    state.comments[postId] || []
  
  // 获取评论数量
  getCommentCount: (state) => (postId: number) => 
    (state.comments[postId] || []).length
}
```

#### Actions

```typescript
{
  // 获取帖子的评论列表
  async fetchComments(postId: number)
  
  // 发表评论
  async createComment(postId: number, content: string)
  
  // 删除评论
  async deleteComment(commentId: number, postId: number)
  
  // 点赞/取消点赞评论
  async toggleCommentLike(commentId: number, postId: number)
  
  // 清空指定帖子的评论
  clearComments(postId: number)
}
```

---

### userStore（用户状态）

**文件**：`stores/user.ts`

**职责**：管理用户个人信息、我的帖子、我的评论

#### State

```typescript
{
  myPosts: Post[]                   // 我的帖子列表
  myComments: Comment[]             // 我的评论列表
  
  stats: {
    postCount: number               // 帖子数
    commentCount: number            // 评论数
  }
  
  loading: boolean
  error: string | null
}
```

#### Getters

```typescript
{
  // 我的帖子
  posts: (state) => state.myPosts
  
  // 我的评论
  comments: (state) => state.myComments
  
  // 统计信息
  statistics: (state) => state.stats
}
```

#### Actions

```typescript
{
  // 获取我的帖子
  async fetchMyPosts()
  
  // 获取我的评论
  async fetchMyComments()
  
  // 获取统计信息
  async fetchStats()
  
  // 更新密码
  async updatePassword(oldPassword: string, newPassword: string)
  
  // 清空用户数据
  clearUserData()
}
```

---

### uiStore（UI状态）

**文件**：`stores/ui.ts`

**职责**：管理全局UI状态（loading、toast、modal等）

#### State

```typescript
{
  globalLoading: boolean            // 全局加载状态
  
  toast: {
    visible: boolean
    message: string
    type: 'success' | 'error' | 'warning' | 'info'
    duration: number
  }
  
  isMobile: boolean                 // 是否移动端
  sidebarCollapsed: boolean         // 侧边栏是否收起（预留）
}
```

#### Getters

```typescript
{
  isLoading: (state) => state.globalLoading
  toastVisible: (state) => state.toast.visible
  deviceType: (state) => state.isMobile ? 'mobile' : 'desktop'
}
```

#### Actions

```typescript
{
  // 显示Toast提示
  showToast(message: string, type: 'success' | 'error' | 'warning' | 'info')
  
  // 隐藏Toast
  hideToast()
  
  // 显示全局Loading
  showLoading()
  
  // 隐藏全局Loading
  hideLoading()
  
  // 更新设备类型
  updateDeviceType()
  
  // 切换侧边栏
  toggleSidebar()
}
```

---

## 5. Axios设计

### 核心配置（request.ts）

**文件**：`api/request.ts`

#### Axios实例创建

```typescript
配置项：
- baseURL: 从环境变量读取（VITE_API_BASE_URL）
- timeout: 10000 (10秒)
- headers: {
    'Content-Type': 'application/json'
  }
```

#### 请求拦截器

**职责**：
1. 自动添加JWT token到请求头
2. 显示全局loading（可选）
3. 请求日志记录（开发环境）

**逻辑流程**：

```typescript
请求拦截器逻辑：

1. 从 authStore 获取 token

2. 如果 token 存在：
   - 添加到请求头：Authorization: `Bearer ${token}`

3. 记录请求信息（开发环境）：
   - console.log(`[API] ${method} ${url}`)

4. 返回配置对象
```

#### 响应拦截器

**职责**：
1. 统一处理响应数据格式
2. 处理业务错误
3. 处理HTTP错误
4. 401自动跳转登录
5. 显示错误提示

**逻辑流程**：

```typescript
响应成功拦截器：

1. 检查 response.data.code

2. 如果 code === 200 或 code === 0：
   - 返回 response.data.data（业务数据）

3. 如果 code !== 200：
   - 抛出业务错误
   - 显示 response.data.message


响应错误拦截器：

1. 判断 error.response.status

2. status === 401（未授权）：
   - 清除本地 token
   - 调用 authStore.clearAuth()
   - 跳转到登录页：router.push('/login')
   - 提示：登录已过期，请重新登录

3. status === 403（无权限）：
   - 提示：无权访问此资源

4. status === 404（不存在）：
   - 提示：请求的资源不存在

5. status === 500（服务器错误）：
   - 提示：服务器错误，请稍后重试

6. 网络错误（error.message === 'Network Error'）：
   - 提示：网络连接失败，请检查网络

7. 超时错误（error.code === 'ECONNABORTED'）：
   - 提示：请求超时，请稍后重试

8. 其他错误：
   - 提示：请求失败，请稍后重试

9. 返回 Promise.reject(error)
```

### 请求/响应数据格式

#### 统一响应格式

```typescript
// 后端返回格式
{
  code: number          // 状态码（200成功，其他失败）
  message: string       // 提示信息
  data: any             // 业务数据
}

// 前端接收格式（拦截器处理后）
直接返回 data 字段的内容
```

#### JWT Token处理

**存储位置**：`localStorage.getItem('campus_tree_token')`

**添加方式**：请求头 `Authorization: Bearer ${token}`

**过期处理**：401响应时自动清除并跳转登录

### 错误处理策略

**分层处理**：
1. **API层**：捕获HTTP错误，返回统一错误对象
2. **Store层**：捕获业务错误，更新error状态
3. **组件层**：展示错误信息给用户

**用户提示**：
- 使用 Element Plus 的 `ElMessage` 组件
- 错误信息显示3秒后自动关闭
- 关键操作失败时保留在界面上

---

## 6. 组件拆分设计

### 布局组件

#### AppHeader（顶部导航栏）

**文件**：`components/layout/AppHeader.vue`

**职责**：
- 显示Logo和产品名称
- 搜索框（V1预留）
- 发布按钮
- 用户头像和下拉菜单

**Props**：无

**Emits**：
- `create-post`：点击发布按钮

**状态**：
- 从 `authStore` 获取用户信息
- 响应式显示（PC端显示完整，移动端简化）

---

#### AppFooter（底部导航栏）

**文件**：`components/layout/AppFooter.vue`

**职责**：
- 移动端底部Tab导航
- 4个导航项：首页、发布、消息（预留）、我的

**Props**：
- `active: string`（当前激活的Tab）

**显示逻辑**：
- 仅在移动端显示（`@media (max-width: 768px)`）
- 固定在底部（`position: fixed`）

---

### 帖子组件

#### PostCard（帖子卡片）

**文件**：`components/post/PostCard.vue`

**职责**：
- 显示单个帖子的预览信息
- 匿名头像、标题、内容摘要、元数据

**Props**：
```typescript
{
  post: Post           // 帖子数据
  showActions: boolean // 是否显示操作按钮（删除等）
}
```

**Emits**：
- `click`：点击卡片
- `like`：点击点赞
- `delete`：删除帖子

**功能**：
- 标题最多显示2行
- 内容最多显示3行
- 相对时间显示
- 点赞数、评论数格式化

---

#### PostList（帖子列表）

**文件**：`components/post/PostList.vue`

**职责**：
- 渲染帖子卡片列表
- 处理无限滚动加载
- 显示空状态和加载状态

**Props**：
```typescript
{
  posts: Post[]        // 帖子数组
  loading: boolean     // 加载状态
  hasMore: boolean     // 是否还有更多
}
```

**Emits**：
- `load-more`：触发加载更多

**功能**：
- 使用 `InfiniteScroll` 组件
- 空状态提示（无帖子时）
- Loading骨架屏

---

#### PostForm（帖子表单）

**文件**：`components/post/PostForm.vue`

**职责**：
- 帖子标题和内容输入
- 表单验证
- 提交发布

**Props**：
```typescript
{
  initialData?: {      // 初始数据（编辑时使用）
    title: string
    content: string
  }
}
```

**Emits**：
- `submit`：提交表单
- `cancel`：取消

**验证规则**：
- 标题：必填，1-100字符
- 内容：必填，10-5000字符

---

### 评论组件

#### CommentList（评论列表）

**文件**：`components/comment/CommentList.vue`

**职责**：
- 渲染评论列表
- 显示评论数量
- 空状态提示

**Props**：
```typescript
{
  postId: number       // 帖子ID
  comments: Comment[]  // 评论数组
  loading: boolean
}
```

**Emits**：
- `delete`：删除评论
- `like`：点赞评论

---

#### CommentItem（单条评论）

**文件**：`components/comment/CommentItem.vue`

**职责**：
- 显示单条评论内容
- 匿名头像、时间、点赞数
- 删除按钮（仅自己的评论）

**Props**：
```typescript
{
  comment: Comment
  canDelete: boolean   // 是否可删除
}
```

**Emits**：
- `delete`：删除
- `like`：点赞

---

#### CommentForm（评论输入框）

**文件**：`components/comment/CommentForm.vue`

**职责**：
- 评论内容输入
- 字数统计
- 提交评论

**Props**：
```typescript
{
  postId: number
  loading: boolean
}
```

**Emits**：
- `submit`：提交评论

**验证规则**：
- 内容：必填，1-500字符

---

### 用户组件

#### UserAvatar（匿名头像）

**文件**：`components/user/UserAvatar.vue`

**职责**：
- 显示匿名用户头像
- 使用emoji或简单图标
- 根据用户ID生成一致的头像

**Props**：
```typescript
{
  userId?: number      // 用户ID（用于生成头像）
  size: 'small' | 'medium' | 'large'
}
```

**实现**：
- 根据 userId 取模，从预设emoji列表中选择
- 确保同一用户始终显示相同头像

---

#### UserInfoCard（用户信息卡片）

**文件**：`components/user/UserInfoCard.vue`

**职责**：
- 显示用户信息
- 用户ID、注册时间、统计信息

**Props**：
```typescript
{
  user: User
  stats: UserStats
}
```

---

### 通用组件

#### LikeButton（点赞按钮）

**文件**：`components/common/LikeButton.vue`

**职责**：
- 显示点赞按钮和点赞数
- 点赞动画效果
- 已点赞/未点赞状态

**Props**：
```typescript
{
  count: number        // 点赞数
  liked: boolean       // 是否已点赞
  disabled: boolean
}
```

**Emits**：
- `toggle`：切换点赞状态

**动画**：
- 点击时放大缩小效果
- 颜色从灰色变为红色

---

#### InfiniteScroll（无限滚动）

**文件**：`components/common/InfiniteScroll.vue`

**职责**：
- 监听滚动事件
- 触底时触发加载更多
- 显示加载状态

**Props**：
```typescript
{
  loading: boolean
  hasMore: boolean
  distance: number     // 触发距离（默认100px）
}
```

**Emits**：
- `load-more`：触发加载

---

#### LoadingSpinner（加载动画）

**文件**：`components/common/LoadingSpinner.vue`

**职责**：显示加载动画

**Props**：
```typescript
{
  size: 'small' | 'medium' | 'large'
  text?: string        // 加载文字
}
```

---

#### EmptyState（空状态）

**文件**：`components/common/EmptyState.vue`

**职责**：显示空状态提示

**Props**：
```typescript
{
  icon?: string        // 图标
  text: string         // 提示文字
  actionText?: string  // 操作按钮文字
}
```

**Emits**：
- `action`：点击操作按钮

---

## 7. API模块设计

### auth.ts（认证接口）

**文件**：`api/auth.ts`

**接口列表**：

```typescript
// 用户登录
login(username: string, password: string)
→ POST /api/auth/login
→ 返回：{ token: string, user: User }

// 用户注册
register(username: string, password: string)
→ POST /api/auth/register
→ 返回：{ token: string, user: User }

// 获取当前用户信息
getCurrentUser()
→ GET /api/auth/me
→ 返回：User

// 登出（前端处理，可选）
logout()
→ 本地清除token
```

---

### post.ts（帖子接口）

**文件**：`api/post.ts`

**接口列表**：

```typescript
// 获取帖子列表（分页）
getPosts(page: number, pageSize: number)
→ GET /api/posts?page=1&page_size=20
→ 返回：{ items: Post[], total: number, page: number, page_size: number }

// 获取帖子详情
getPostById(id: number)
→ GET /api/posts/:id
→ 返回：Post

// 创建帖子
createPost(data: { title: string, content: string })
→ POST /api/posts
→ 返回：Post

// 删除帖子
deletePost(id: number)
→ DELETE /api/posts/:id
→ 返回：{ message: string }

// 点赞帖子
likePost(id: number)
→ POST /api/posts/:id/like
→ 返回：{ liked: boolean, like_count: number }

// 取消点赞帖子
unlikePost(id: number)
→ DELETE /api/posts/:id/like
→ 返回：{ liked: boolean, like_count: number }
```

---

### comment.ts（评论接口）

**文件**：`api/comment.ts`

**接口列表**：

```typescript
// 获取帖子的评论列表
getComments(postId: number)
→ GET /api/posts/:postId/comments
→ 返回：Comment[]

// 创建评论
createComment(postId: number, content: string)
→ POST /api/posts/:postId/comments
→ 返回：Comment

// 删除评论
deleteComment(commentId: number)
→ DELETE /api/comments/:commentId
→ 返回：{ message: string }

// 点赞评论
likeComment(commentId: number)
→ POST /api/comments/:commentId/like
→ 返回：{ liked: boolean, like_count: number }

// 取消点赞评论
unlikeComment(commentId: number)
→ DELETE /api/comments/:commentId/like
→ 返回：{ liked: boolean, like_count: number }
```

---

### user.ts（用户接口）

**文件**：`api/user.ts`

**接口列表**：

```typescript
// 获取我的帖子
getMyPosts()
→ GET /api/users/me/posts
→ 返回：Post[]

// 获取我的评论
getMyComments()
→ GET /api/users/me/comments
→ 返回：Comment[]

// 获取用户统计信息
getUserStats()
→ GET /api/users/me/stats
→ 返回：{ post_count: number, comment_count: number }

// 修改密码
updatePassword(oldPassword: string, newPassword: string)
→ PUT /api/users/me/password
→ 返回：{ message: string }
```

---

## 8. 数据流设计

### 用户登录流程

```
[LoginView 组件]
       ↓
1. 用户输入用户名和密码
       ↓
2. 点击登录按钮
       ↓
3. 调用 authStore.login(username, password)
       ↓
4. authStore 调用 api/auth.login()
       ↓
5. Axios 发送 POST /api/auth/login
       ↓
6. 请求拦截器：记录日志（无需添加token）
       ↓
7. 后端验证用户名密码
       ↓
8. 响应拦截器：检查状态码
       ↓
9. 成功：返回 { token, user }
       ↓
10. authStore 更新状态：
    - state.token = token
    - state.user = user
    - state.isAuthenticated = true
    - localStorage.setItem('campus_tree_token', token)
       ↓
11. 组件接收成功信号
       ↓
12. 显示成功提示（ElMessage.success）
       ↓
13. 路由跳转到首页或 redirect 参数指定页面
       ↓
14. 首页开始加载数据


失败流程：
       ↓
8. 响应拦截器：检测到错误
       ↓
9. 显示错误提示（ElMessage.error）
       ↓
10. 组件显示错误状态
       ↓
11. 用户可重新尝试
```

---

### 浏览帖子流程

```
[HomeView 组件加载]
       ↓
1. onMounted 钩子触发
       ↓
2. 调用 postStore.fetchPosts(1)
       ↓
3. postStore 调用 api/post.getPosts(1, 20)
       ↓
4. Axios 发送 GET /api/posts?page=1&page_size=20
       ↓
5. 请求拦截器：
    - 从 authStore 获取 token
    - 添加 Authorization: Bearer ${token}
       ↓
6. 后端查询数据库
       ↓
7. 响应拦截器：处理响应
       ↓
8. 成功：返回 { items: Post[], total, page, page_size }
       ↓
9. postStore 更新状态：
    - state.posts = items
    - state.pagination = { page, pageSize, total, hasMore }
    - state.loading = false
       ↓
10. 组件响应式更新：
    - PostList 接收 posts 数组
    - 渲染 PostCard 组件列表
       ↓
11. 用户看到帖子列表


无限滚动加载更多：
       ↓
1. 用户滚动到底部
       ↓
2. InfiniteScroll 组件触发 @load-more
       ↓
3. HomeView 调用 postStore.loadMorePosts()
       ↓
4. postStore 调用 api/post.getPosts(page + 1, 20)
       ↓
5. 响应成功后追加数据：
    - state.posts.push(...newItems)
    - state.pagination.page++
    - state.pagination.hasMore = (newItems.length === pageSize)
       ↓
6. PostList 自动渲染新帖子
```

---

### 点赞帖子流程

```
[用户点击点赞按钮]
       ↓
1. PostCard 组件接收点击事件
       ↓
2. 触发 @like emit
       ↓
3. 父组件调用 postStore.toggleLike(postId)
       ↓
4. postStore 判断当前点赞状态：
    - 如果已点赞：调用 api/post.unlikePost(postId)
    - 如果未点赞：调用 api/post.likePost(postId)
       ↓
5. Axios 发送请求：
    - POST /api/posts/:id/like  或
    - DELETE /api/posts/:id/like
       ↓
6. 请求拦截器：添加 token
       ↓
7. 后端更新点赞记录
       ↓
8. 响应拦截器：处理响应
       ↓
9. 成功：返回 { liked: boolean, like_count: number }
       ↓
10. postStore 更新对应帖子的状态：
    const post = state.posts.find(p => p.id === postId)
    if (post) {
      post.is_liked = liked
      post.like_count = like_count
    }
       ↓
11. 组件响应式更新：
    - LikeButton 显示新的点赞数
    - 图标颜色变化（灰色 ↔ 红色）
    - 播放点赞动画
       ↓
12. 用户看到点赞效果


乐观更新策略（可选优化）：
       ↓
1. 用户点击点赞
       ↓
2. 立即更新UI（不等待请求）：
    - liked = !liked
    - like_count += liked ? 1 : -1
       ↓
3. 发送API请求
       ↓
4. 请求成功：保持UI状态
       ↓
5. 请求失败：回滚UI状态
    - liked = !liked
    - like_count += liked ? 1 : -1
    - 显示错误提示
```

---

### 查看帖子详情并评论流程

```
[用户点击帖子卡片]
       ↓
1. PostCard 触发 @click
       ↓
2. 路由跳转：router.push(`/post/${postId}`)
       ↓
3. PostDetailView 组件加载
       ↓
4. onMounted 钩子触发
       ↓
5. 并发请求：
    - postStore.fetchPostDetail(postId)
    - commentStore.fetchComments(postId)
       ↓
6. postStore 调用 api/post.getPostById(postId)
   commentStore 调用 api/comment.getComments(postId)
       ↓
7. Axios 发送请求：
    - GET /api/posts/:id
    - GET /api/posts/:postId/comments
       ↓
8. 请求拦截器：添加 token
       ↓
9. 后端查询数据
       ↓
10. 响应拦截器：处理响应
       ↓
11. 成功：
    - postStore.state.currentPost = post
    - commentStore.state.comments[postId] = comments
       ↓
12. 组件渲染：
    - 显示帖子详情（标题、内容、元数据）
    - 显示点赞按钮
    - 显示评论列表
    - 显示评论输入框
       ↓
13. 用户看到完整帖子和评论


发表评论：
       ↓
1. 用户在 CommentForm 输入评论内容
       ↓
2. 点击发送按钮
       ↓
3. 表单验证：
    - 检查内容是否为空
    - 检查长度（1-500字符）
       ↓
4. 验证通过，CommentForm 触发 @submit
       ↓
5. PostDetailView 调用 commentStore.createComment(postId, content)
       ↓
6. commentStore 调用 api/comment.createComment(postId, content)
       ↓
7. Axios 发送 POST /api/posts/:postId/comments
       ↓
8. 请求拦截器：添加 token
       ↓
9. 后端创建评论记录
       ↓
10. 响应拦截器：处理响应
       ↓
11. 成功：返回新创建的 Comment
       ↓
12. commentStore 更新状态：
    - state.comments[postId].unshift(newComment)  // 新评论插入顶部
       ↓
13. postStore 更新帖子评论数：
    - state.currentPost.comment_count++
       ↓
14. 组件更新：
    - CommentList 渲染新评论
    - CommentForm 清空输入框
    - 显示成功提示
       ↓
15. 用户看到自己的评论出现在列表顶部
```

---

### 数据流最佳实践

#### 1. 单向数据流

```
Store (状态源) → 组件 (消费者) → 用户交互 → Action → Store
```

**原则**：
- 组件不直接修改 store 状态
- 通过 actions 触发状态变更
- 状态变化自动触发组件更新

#### 2. 异步操作处理

```typescript
// 标准异步 action 模式

async fetchData() {
  this.loading = true
  this.error = null
  
  try {
    const data = await api.getData()
    this.data = data
  } catch (error) {
    this.error = error.message
    // 显示错误提示
    ElMessage.error(error.message)
  } finally {
    this.loading = false
  }
}
```

#### 3. 错误边界

**分层处理**：
- **API层**：捕获网络错误，返回统一错误格式
- **Store层**：更新error状态，触发UI提示
- **组件层**：显示错误信息，提供重试操作

#### 4. Loading状态管理

**局部Loading**：
- 在对应的 store 中管理
- 例如：`postStore.loading`

**全局Loading**：
- 在 `uiStore` 中管理
- 用于页面级加载

#### 5. 缓存策略

**帖子列表缓存**：
- 首次加载后缓存在 `postStore.posts`
- 下拉刷新时清空并重新加载
- 返回首页时保持滚动位置和数据

**帖子详情缓存**：
- 存储在 `postStore.currentPost`
- 切换帖子时更新
- 可扩展为Map缓存多个帖子

---

## 9. 开发规范

### 命名规范

**组件命名**：
- 大驼峰（PascalCase）：`PostCard.vue`
- 多单词组成：`UserInfoCard.vue`

**文件命名**：
- 小驼峰（camelCase）：`usePost.ts`
- 中划线（kebab-case）：`post-list.css`

**变量命名**：
- 小驼峰：`const userName = 'xxx'`
- 布尔值以 is/has/can 开头：`isLoading`, `hasMore`

**常量命名**：
- 全大写下划线：`const MAX_POST_LENGTH = 5000`

### 代码组织

**Vue组件结构**：
```vue
<script setup lang="ts">
// 1. 导入依赖
// 2. 定义 props 和 emits
// 3. 响应式数据
// 4. 计算属性
// 5. 方法
// 6. 生命周期钩子
// 7. 侦听器
</script>

<template>
  <!-- 模板 -->
</template>

<style scoped>
  /* 样式 */
</style>
```

**Store结构**：
```typescript
export const useXxxStore = defineStore('xxx', () => {
  // 1. State
  const data = ref()
  
  // 2. Getters
  const computedData = computed(() => ...)
  
  // 3. Actions
  async function fetchData() { ... }
  
  // 4. 返回
  return {
    data,
    computedData,
    fetchData
  }
})
```

### 注释规范

**函数注释**：
```typescript
/**
 * 获取帖子列表
 * @param page 页码
 * @param pageSize 每页数量
 * @returns 帖子列表
 */
async function getPosts(page: number, pageSize: number): Promise<Post[]> {
  // ...
}
```

**组件注释**：
```vue
<script setup lang="ts">
/**
 * PostCard - 帖子卡片组件
 * 
 * 功能：
 * - 显示帖子预览信息
 * - 支持点赞和点击跳转
 * 
 * 使用：
 * <PostCard :post="post" @click="handleClick" />
 */
</script>
```

### Git提交规范

**提交信息格式**：
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type类型**：
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档修改
- `style`: 代码格式调整
- `refactor`: 重构
- `perf`: 性能优化
- `test`: 测试
- `chore`: 构建/工具链

**示例**：
```
feat(post): 实现帖子列表无限滚动

- 添加 InfiniteScroll 组件
- 在 PostList 中集成无限滚动
- 更新 postStore 的 loadMorePosts action

Closes #123
```

---

## 10. 性能优化建议

### 组件优化

**懒加载**：
```typescript
// 路由懒加载
component: () => import('@/views/home/HomeView.vue')

// 组件懒加载
const PostDetail = defineAsyncComponent(() => 
  import('@/components/post/PostDetail.vue')
)
```

**列表渲染优化**：
```vue
<!-- 使用 key 优化 v-for -->
<PostCard
  v-for="post in posts"
  :key="post.id"
  :post="post"
/>
```

### 网络优化

**请求合并**：
- 使用 `Promise.all` 并发请求
- 避免瀑布流请求

**防抖节流**：
- 搜索框使用防抖（debounce）
- 滚动事件使用节流（throttle）

### 打包优化

**代码分割**：
- 路由级别代码分割
- 第三方库按需引入

**资源压缩**：
- 图片压缩和使用WebP格式
- CSS/JS压缩

---

## 11. 测试策略

### 单元测试

**测试工具**：Vitest

**测试覆盖**：
- 工具函数（utils/）
- Store逻辑（stores/）
- 组合式函数（composables/）

### 组件测试

**测试工具**：Vue Test Utils + Vitest

**测试重点**：
- 组件渲染
- Props传递
- 事件触发
- 用户交互

### E2E测试

**测试工具**：Playwright（可选）

**测试场景**：
- 用户登录流程
- 发布帖子流程
- 评论互动流程

---

## 12. 部署方案

### 环境变量

**.env.development**：
```
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_TITLE=CampusTree
```

**.env.production**：
```
VITE_API_BASE_URL=https://api.campustree.com
VITE_APP_TITLE=CampusTree
```

### 构建命令

```bash
# 开发环境
npm run dev

# 生产构建
npm run build

# 预览构建结果
npm run preview
```

### Nginx配置

```nginx
server {
  listen 80;
  server_name campustree.com;
  
  root /var/www/campustree/dist;
  index index.html;
  
  # SPA路由支持
  location / {
    try_files $uri $uri/ /index.html;
  }
  
  # API代理
  location /api {
    proxy_pass http://localhost:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
  }
  
  # 静态资源缓存
  location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
  }
}
```

---

## 总结

CampusTree 前端架构的核心特点：

### 技术选型
- **Vue3 + TypeScript**：类型安全 + 组合式API
- **Pinia**：轻量级状态管理
- **Element Plus**：成熟的组件库
- **Vite**：快速构建工具

### 架构原则
1. **模块化**：按功能领域划分目录
2. **单一职责**：组件和函数职责清晰
3. **可维护**：统一的命名和代码规范
4. **可扩展**：预留扩展点，便于迭代

### 数据流
- **单向数据流**：Store → Component → Action → Store
- **分层错误处理**：API层、Store层、组件层
- **统一状态管理**：Pinia管理所有业务状态

### 开发流程
1. 设计组件和API接口
2. 实现Store状态管理
3. 开发页面和组件
4. 编写测试用例
5. 优化性能和体验
6. 部署上线

这份架构设计为前端开发提供了清晰的技术蓝图，可以确保团队协作高效、代码质量稳定。

---

**文档版本**：V1.0  
**创建日期**：2026-06-17  
**维护者**：CampusTree前端团队