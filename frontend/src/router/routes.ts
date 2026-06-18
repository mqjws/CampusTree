import type { RouteRecordRaw } from 'vue-router'

const systemPage = () => import('@/views/system/SystemPageView.vue')
const loginPage = () => import('@/views/auth/LoginView.vue')
const registerPage = () => import('@/views/auth/RegisterView.vue')
const homePage = () => import('@/views/home/HomeView.vue')
const postDetailPage = () => import('@/views/post/PostDetailView.vue')
const createPostPage = () => import('@/views/post/CreatePostView.vue')
const profilePage = () => import('@/views/profile/ProfileView.vue')

export const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: homePage,
    meta: {
      title: 'CampusTree',
      requiresAuth: true,
    },
  },
  {
    path: '/login',
    name: 'Login',
    component: loginPage,
    meta: {
      title: '登录 - CampusTree',
      requiresAuth: false,
    },
  },
  {
    path: '/register',
    name: 'Register',
    component: registerPage,
    meta: {
      title: '注册 - CampusTree',
      requiresAuth: false,
    },
  },
  {
    path: '/post/:id',
    name: 'PostDetail',
    component: postDetailPage,
    meta: {
      title: '帖子详情 - CampusTree',
      requiresAuth: true,
    },
  },
  {
    path: '/create',
    name: 'CreatePost',
    component: createPostPage,
    meta: {
      title: '发布帖子 - CampusTree',
      requiresAuth: true,
    },
  },
  {
    path: '/profile',
    name: 'Profile',
    component: profilePage,
    meta: {
      title: '用户中心 - CampusTree',
      requiresAuth: true,
    },
  },
  {
    path: '/profile/posts',
    name: 'MyPosts',
    component: profilePage,
    meta: {
      title: '我的帖子 - CampusTree',
      requiresAuth: true,
    },
  },
  {
    path: '/profile/comments',
    name: 'MyComments',
    component: profilePage,
    meta: {
      title: '我的评论 - CampusTree',
      requiresAuth: true,
    },
  },
  {
    path: '/profile/settings',
    name: 'Settings',
    component: profilePage,
    meta: {
      title: '设置 - CampusTree',
      requiresAuth: true,
    },
  },
  {
    path: '/error',
    name: 'Error',
    component: systemPage,
    meta: {
      title: '系统错误 - CampusTree',
      requiresAuth: false,
      placeholder: 'Error',
    },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: systemPage,
    meta: {
      title: '页面不存在 - CampusTree',
      requiresAuth: false,
      placeholder: 'NotFound',
    },
  },
]
