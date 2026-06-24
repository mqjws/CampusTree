<script setup lang="ts">
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage, ElMessageBox } from 'element-plus'
import { computed, onMounted, reactive, ref } from 'vue'
import {
  Calendar,
  ChatDotRound,
  Delete,
  EditPen,
  MessageBox,
  Pointer,
  Setting,
  Tickets,
  User,
  View,
} from '@element-plus/icons-vue'
import { useRoute, useRouter } from 'vue-router'
import AppLayout from '@/components/layout/AppLayout.vue'
import CommentList from '@/components/comment/CommentList.vue'
import PostCard from '@/components/post/PostCard.vue'
import { useAuthStore } from '@/stores/modules/auth'
import { useUserStore } from '@/stores/modules/user'
import * as postApi from '@/api/post'
import * as userApi from '@/api/user'
import type { PostRecord } from '@/types/content'
import { formatFullTime, formatRelativeTime } from '@/utils/format'

interface PasswordForm {
  oldPassword: string
  newPassword: string
  confirmPassword: string
}

interface ProfileForm {
  nickname: string
}

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const authStore = useAuthStore()
const passwordFormRef = ref<FormInstance>()
const profileFormRef = ref<FormInstance>()
const passwordSubmitting = ref(false)
const profileSubmitting = ref(false)

const passwordForm = reactive<PasswordForm>({
  oldPassword: '',
  newPassword: '',
  confirmPassword: '',
})

const profileForm = reactive<ProfileForm>({
  nickname: '',
})

const profileRules: FormRules<ProfileForm> = {
  nickname: [
    { required: true, message: '请输入昵称', trigger: 'blur' },
    { min: 1, max: 50, message: '昵称需在 1 到 50 个字符之间', trigger: 'blur' },
  ],
}

const passwordRules: FormRules<PasswordForm> = {
  oldPassword: [{ required: true, message: '请输入当前密码', trigger: 'blur' }],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '新密码至少 6 位', trigger: 'blur' },
  ],
  confirmPassword: [
    { required: true, message: '请再次输入新密码', trigger: 'blur' },
    {
      validator: (_rule, value: string, callback) => {
        if (value !== passwordForm.newPassword) {
          callback(new Error('两次输入的新密码不一致'))
          return
        }

        callback()
      },
      trigger: ['blur', 'change'],
    },
  ],
}

const section = computed(() => {
  if (route.path === '/profile/posts') {
    return 'posts'
  }

  if (route.path === '/profile/comments') {
    return 'comments'
  }

  if (route.path === '/profile/settings') {
    return 'settings'
  }

  return 'overview'
})

const sectionCopy = computed(() => {
  const map = {
    overview: '查看账号资料、内容统计、最近动态和常用操作。',
    posts: '这里展示当前登录用户发布的真实帖子列表。',
    comments: '这里展示当前登录用户发表的真实评论列表。',
    settings: '设置页已补齐最小可用功能：修改密码、清理缓存、退出登录。',
  }

  return map[section.value]
})

const latestActivity = computed(() => {
  const dates = [
    userStore.profile.stats.latestPostAt,
    userStore.profile.stats.latestCommentAt,
  ].filter(Boolean) as string[]

  if (dates.length === 0) {
    return null
  }

  return dates.sort((a, b) => new Date(b).getTime() - new Date(a).getTime())[0]
})

const latestActivityText = computed(() => {
  return latestActivity.value ? formatRelativeTime(latestActivity.value) : '暂无动态'
})

const activityTotalScore = computed(() => {
  return userStore.myActivity.reduce((total, item) => total + item.score, 0)
})

const activeDays = computed(() => {
  return userStore.myActivity.filter((item) => item.score > 0).length
})

onMounted(() => {
  userStore
    .fetchCurrentUser()
    .then(syncProfileForm)
    .catch(() => undefined)
  userStore.fetchMyPosts().catch(() => undefined)
  userStore.fetchMyComments().catch(() => undefined)
  userStore.fetchMyStats().catch(() => undefined)
  userStore.fetchMyActivity(90).catch(() => undefined)
})

function syncProfileForm() {
  profileForm.nickname = userStore.currentUser?.nickname || ''
}

function openPost(id: number) {
  router.push(`/post/${id}`)
}

function getActivityLevel(score: number): number {
  if (score <= 0) {
    return 0
  }

  if (score <= 2) {
    return 1
  }

  if (score <= 5) {
    return 2
  }

  if (score <= 9) {
    return 3
  }

  return 4
}

function formatActivityTitle(item: {
  date: string
  postCount: number
  commentCount: number
  likeCount: number
  score: number
}) {
  return `${item.date} 活跃度 ${item.score}：发帖 ${item.postCount}，评论 ${item.commentCount}，点赞 ${item.likeCount}`
}

async function handleUpdateProfile() {
  const isValid = await profileFormRef.value?.validate().catch(() => false)

  if (!isValid) {
    return
  }

  profileSubmitting.value = true

  try {
    await userStore.updateMyProfile(profileForm.nickname.trim())
    syncProfileForm()
    ElMessage.success('昵称已更新')
  } catch {
    ElMessage.error('昵称更新失败，请稍后重试')
  } finally {
    profileSubmitting.value = false
  }
}

async function handleUpdatePassword() {
  const isValid = await passwordFormRef.value?.validate().catch(() => false)

  if (!isValid) {
    return
  }

  passwordSubmitting.value = true

  try {
    await userApi.updateMyPassword({
      old_password: passwordForm.oldPassword,
      new_password: passwordForm.newPassword,
    })

    passwordForm.oldPassword = ''
    passwordForm.newPassword = ''
    passwordForm.confirmPassword = ''
    ElMessage.success('密码修改成功')
  } catch {
    ElMessage.error('密码修改失败，请确认当前密码是否正确')
  } finally {
    passwordSubmitting.value = false
  }
}

function handleClearCache() {
  localStorage.removeItem('campus_tree_token')
  authStore.clearAuth()
  ElMessage.success('本地缓存已清理')
  router.push('/login')
}

async function handleLogout() {
  try {
    await ElMessageBox.confirm('确认退出当前登录状态吗？', '退出登录', {
      type: 'warning',
      confirmButtonText: '退出',
      cancelButtonText: '取消',
    })

    authStore.clearAuth()
    ElMessage.success('已退出登录')
    router.push('/login')
  } catch {
    return
  }
}

async function handleDeleteMyPost(post: PostRecord) {
  try {
    await ElMessageBox.confirm(`确认删除帖子「${post.title}」？`, '删除确认', {
      type: 'warning',
      confirmButtonText: '删除',
      cancelButtonText: '取消',
    })
    await postApi.deletePost(post.id)
    userStore.myPosts = userStore.myPosts.filter((item) => item.id !== post.id)
    await userStore.fetchMyStats().catch(() => undefined)
    ElMessage.success('帖子已删除')
  } catch {
    // 用户取消或删除失败
  }
}
</script>

<template>
  <AppLayout
    title="用户中心"
    :description="sectionCopy"
    :user-card="{
      nickname: userStore.profile.nickname,
      userId: userStore.profile.userId,
      tagline: userStore.profile.tagline,
    }"
  >
    <section class="profile-overview">
      <div class="profile-overview__identity">
        <span class="profile-overview__avatar">🫧</span>
        <div>
          <h2>{{ userStore.profile.nickname }}</h2>
          <p>{{ userStore.profile.userId }} · 注册于 {{ userStore.profile.joinedAt }}</p>
          <span>{{ userStore.profile.tagline }}</span>
        </div>
      </div>

      <div class="profile-overview__stats">
        <article>
          <strong>{{ userStore.profile.stats.posts }}</strong>
          <span>我的帖子</span>
        </article>
        <article>
          <strong>{{ userStore.profile.stats.comments }}</strong>
          <span>我的评论</span>
        </article>
        <article>
          <strong>{{ userStore.profile.stats.likes }}</strong>
          <span>收到互动</span>
        </article>
      </div>
    </section>

    <section class="profile-nav">
      <el-button
        :type="section === 'overview' ? 'primary' : 'default'"
        size="large"
        @click="router.push('/profile')"
      >
        <el-icon><Tickets /></el-icon>
        概览
      </el-button>
      <el-button
        :type="section === 'posts' ? 'primary' : 'default'"
        size="large"
        @click="router.push('/profile/posts')"
      >
        <el-icon><EditPen /></el-icon>
        我的帖子
      </el-button>
      <el-button
        :type="section === 'comments' ? 'primary' : 'default'"
        size="large"
        @click="router.push('/profile/comments')"
      >
        <el-icon><MessageBox /></el-icon>
        我的评论
      </el-button>
      <el-button
        :type="section === 'settings' ? 'primary' : 'default'"
        size="large"
        @click="router.push('/profile/settings')"
      >
        <el-icon><Setting /></el-icon>
        设置
      </el-button>
    </section>

    <section v-if="section === 'overview'" class="profile-panels">
      <article class="profile-panel profile-panel--summary">
        <div>
          <h2>资料摘要</h2>
          <p>登录身份和公开昵称分开展示，昵称会用于帖子作者名。</p>
        </div>
        <div class="profile-summary-grid">
          <div>
            <span>公开昵称</span>
            <strong>{{ userStore.profile.nickname }}</strong>
          </div>
          <div>
            <span>用户名</span>
            <strong>{{ userStore.currentUser?.username || '--' }}</strong>
          </div>
          <div>
            <span>邮箱</span>
            <strong>{{ userStore.currentUser?.email || '--' }}</strong>
          </div>
          <div>
            <span>注册时间</span>
            <strong>{{ userStore.profile.joinedAt }}</strong>
          </div>
        </div>
      </article>

      <section class="profile-overview-grid">
        <article class="profile-panel">
          <h2>内容统计</h2>
          <div class="profile-metric-list">
            <div>
              <el-icon><Tickets /></el-icon>
              <span>发布帖子</span>
              <strong>{{ userStore.profile.stats.posts }}</strong>
            </div>
            <div>
              <el-icon><ChatDotRound /></el-icon>
              <span>发表评论</span>
              <strong>{{ userStore.profile.stats.comments }}</strong>
            </div>
            <div>
              <el-icon><Pointer /></el-icon>
              <span>收到互动</span>
              <strong>{{ userStore.profile.stats.likes }}</strong>
            </div>
            <div>
              <el-icon><View /></el-icon>
              <span>内容浏览</span>
              <strong>{{ userStore.profile.stats.views }}</strong>
            </div>
          </div>
        </article>

        <article class="profile-panel">
          <h2>活跃度摘要</h2>
          <div class="profile-activity">
            <div>
              <el-icon><Calendar /></el-icon>
              <span>最近动态</span>
              <strong>{{ latestActivityText }}</strong>
            </div>
            <p>
              最近发帖：
              {{
                userStore.profile.stats.latestPostAt
                  ? formatFullTime(userStore.profile.stats.latestPostAt)
                  : '暂无'
              }}
            </p>
            <p>
              最近评论：
              {{
                userStore.profile.stats.latestCommentAt
                  ? formatFullTime(userStore.profile.stats.latestCommentAt)
                  : '暂无'
              }}
            </p>
          </div>
        </article>
      </section>

      <article class="profile-panel">
        <div class="profile-panel__header">
          <div>
            <h2>最近 90 天活跃度</h2>
            <p>发帖、评论和点赞会计入活跃度。</p>
          </div>
          <div class="profile-heatmap__summary">
            <strong>{{ activeDays }}</strong>
            <span>活跃天数</span>
            <strong>{{ activityTotalScore }}</strong>
            <span>总分</span>
          </div>
        </div>

        <el-empty v-if="userStore.myActivity.length === 0" description="暂无活跃度数据" />
        <div v-else class="profile-heatmap">
          <div
            v-for="item in userStore.myActivity"
            :key="item.date"
            class="profile-heatmap__cell"
            :class="`profile-heatmap__cell--${getActivityLevel(item.score)}`"
            :title="formatActivityTitle(item)"
          />
        </div>
        <div class="profile-heatmap__legend">
          <span>少</span>
          <i class="profile-heatmap__cell profile-heatmap__cell--0" />
          <i class="profile-heatmap__cell profile-heatmap__cell--1" />
          <i class="profile-heatmap__cell profile-heatmap__cell--2" />
          <i class="profile-heatmap__cell profile-heatmap__cell--3" />
          <i class="profile-heatmap__cell profile-heatmap__cell--4" />
          <span>多</span>
        </div>
      </article>

      <article class="profile-panel">
        <h2>快捷操作</h2>
        <div class="profile-actions">
          <el-button size="large" @click="router.push('/profile/settings')">
            <el-icon><User /></el-icon>
            修改昵称
          </el-button>
          <el-button size="large" @click="router.push('/profile/settings')">
            <el-icon><Setting /></el-icon>
            修改密码
          </el-button>
          <el-button size="large" @click="router.push('/profile/posts')">
            <el-icon><EditPen /></el-icon>
            我的帖子
          </el-button>
          <el-button size="large" @click="router.push('/profile/comments')">
            <el-icon><MessageBox /></el-icon>
            我的评论
          </el-button>
        </div>
      </article>
    </section>

    <section v-else-if="section === 'posts'" class="profile-panels">
      <el-empty v-if="userStore.myPosts.length === 0" description="当前用户还没有发布帖子" />
      <div v-else class="profile-post-list">
        <article v-for="post in userStore.myPosts" :key="post.id" class="profile-post-item">
          <PostCard :post="post" @select="openPost" />
          <div class="profile-post-item__actions">
            <el-button type="danger" plain :icon="Delete" @click="handleDeleteMyPost(post)">
              删除
            </el-button>
          </div>
        </article>
      </div>
    </section>

    <section v-else-if="section === 'comments'" class="profile-panels">
      <CommentList :comments="userStore.myComments" title="我的评论" />
    </section>

    <section v-else class="profile-settings">
      <article class="profile-panel">
        <h2>账号设置</h2>
        <p>当前可修改昵称、密码，或清理本地登录状态。</p>
      </article>

      <article class="profile-setting-card">
        <h3>个人资料</h3>
        <el-form
          ref="profileFormRef"
          :model="profileForm"
          :rules="profileRules"
          label-position="top"
        >
          <el-form-item label="昵称" prop="nickname">
            <el-input v-model.trim="profileForm.nickname" maxlength="50" show-word-limit />
          </el-form-item>
          <el-button
            type="primary"
            size="large"
            :loading="profileSubmitting"
            @click="handleUpdateProfile"
          >
            保存昵称
          </el-button>
        </el-form>
      </article>

      <article class="profile-setting-card">
        <h3>修改密码</h3>
        <el-form
          ref="passwordFormRef"
          :model="passwordForm"
          :rules="passwordRules"
          label-position="top"
        >
          <el-form-item label="当前密码" prop="oldPassword">
            <el-input v-model="passwordForm.oldPassword" type="password" show-password />
          </el-form-item>
          <el-form-item label="新密码" prop="newPassword">
            <el-input v-model="passwordForm.newPassword" type="password" show-password />
          </el-form-item>
          <el-form-item label="确认新密码" prop="confirmPassword">
            <el-input v-model="passwordForm.confirmPassword" type="password" show-password />
          </el-form-item>
          <el-button
            type="primary"
            size="large"
            :loading="passwordSubmitting"
            @click="handleUpdatePassword"
          >
            保存新密码
          </el-button>
        </el-form>
      </article>

      <div class="profile-settings__grid">
        <article class="profile-setting-card">
          <h3>清理缓存</h3>
          <p>清理当前浏览器中的本地登录缓存，并返回登录页。</p>
          <el-button plain size="large" @click="handleClearCache">清理缓存</el-button>
        </article>
        <article class="profile-setting-card profile-setting-card--danger">
          <h3>退出登录</h3>
          <p>清除当前登录状态并返回登录页。</p>
          <el-button type="danger" size="large" @click="handleLogout">退出登录</el-button>
        </article>
      </div>
    </section>
  </AppLayout>
</template>

<style scoped>
.profile-overview,
.profile-nav,
.profile-panel,
.profile-setting-card {
  padding: var(--space-24);
  border: 1px solid rgba(229, 231, 235, 0.76);
  border-radius: var(--radius-16);
  background: rgba(255, 255, 255, 0.94);
  box-shadow: var(--shadow-card);
}

.profile-overview {
  display: grid;
  gap: var(--space-24);
}

.profile-overview__identity {
  display: flex;
  align-items: center;
  gap: var(--space-16);
}

.profile-overview__avatar {
  display: grid;
  place-items: center;
  width: 64px;
  height: 64px;
  border-radius: 20px;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.18), rgba(59, 130, 246, 0.14));
  font-size: 28px;
}

.profile-overview__identity h2 {
  margin-bottom: var(--space-8);
  color: var(--color-text-primary);
  font-size: 24px;
  font-weight: 700;
}

.profile-overview__identity p,
.profile-overview__identity span,
.profile-panel p,
.profile-setting-card p {
  color: var(--color-text-secondary);
  font-size: 14px;
  line-height: 1.7;
}

.profile-overview__stats {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--space-16);
}

.profile-overview__stats article {
  padding: var(--space-16);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-12);
  background: linear-gradient(180deg, #ffffff 0%, #f8fcfa 100%);
}

.profile-overview__stats strong {
  display: block;
  margin-bottom: var(--space-8);
  color: var(--color-text-primary);
  font-size: 24px;
}

.profile-overview__stats span {
  color: var(--color-text-secondary);
  font-size: 13px;
}

.profile-nav {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-12);
}

.profile-panels,
.profile-settings {
  display: grid;
  gap: var(--space-16);
}

.profile-post-list {
  display: grid;
  gap: var(--space-16);
}

.profile-post-item {
  display: grid;
  gap: var(--space-8);
}

.profile-post-item__actions {
  display: flex;
  justify-content: flex-end;
}

.profile-overview-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--space-16);
}

.profile-panel--summary {
  display: grid;
  gap: var(--space-16);
}

.profile-panel__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-12);
  margin-bottom: var(--space-16);
}

.profile-panel h2,
.profile-setting-card h3 {
  margin-bottom: var(--space-8);
  color: var(--color-text-primary);
  font-size: 18px;
  font-weight: 600;
}

.profile-panel__header h2 {
  margin-bottom: 0;
}

.profile-summary-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: var(--space-12);
}

.profile-summary-grid div,
.profile-metric-list div,
.profile-activity div {
  min-width: 0;
  padding: var(--space-16);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-12);
  background: linear-gradient(180deg, #ffffff 0%, #f8fcfa 100%);
}

.profile-summary-grid span,
.profile-metric-list span,
.profile-activity span {
  display: block;
  margin-bottom: var(--space-8);
  color: var(--color-text-secondary);
  font-size: 13px;
}

.profile-summary-grid strong,
.profile-metric-list strong,
.profile-activity strong {
  display: block;
  overflow: hidden;
  color: var(--color-text-primary);
  font-size: 16px;
  font-weight: 600;
  line-height: 1.5;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.profile-summary-grid strong {
  overflow: visible;
  overflow-wrap: anywhere;
  text-overflow: clip;
  white-space: normal;
}

.profile-metric-list {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--space-12);
}

.profile-metric-list div {
  display: grid;
  gap: var(--space-4);
}

.profile-metric-list .el-icon,
.profile-activity .el-icon {
  color: var(--color-primary);
  font-size: 20px;
}

.profile-metric-list strong {
  font-size: 24px;
}

.profile-activity {
  display: grid;
  gap: var(--space-12);
}

.profile-activity div {
  display: grid;
  gap: var(--space-4);
}

.profile-heatmap {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(14px, 1fr));
  gap: 6px;
  padding: var(--space-16);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-12);
  background: linear-gradient(180deg, #ffffff 0%, #f8fcfa 100%);
}

.profile-heatmap__summary {
  display: grid;
  grid-template-columns: repeat(2, auto);
  align-items: baseline;
  gap: var(--space-4) var(--space-8);
  color: var(--color-text-secondary);
  font-size: 13px;
  text-align: right;
}

.profile-heatmap__summary strong {
  color: var(--color-text-primary);
  font-size: 18px;
}

.profile-heatmap__cell {
  display: block;
  aspect-ratio: 1;
  min-width: 10px;
  border: 1px solid rgba(229, 231, 235, 0.8);
  border-radius: 4px;
}

.profile-heatmap__cell--0 {
  background: #eef2f7;
}

.profile-heatmap__cell--1 {
  background: #d1fae5;
}

.profile-heatmap__cell--2 {
  background: #86efac;
}

.profile-heatmap__cell--3 {
  background: #22c55e;
}

.profile-heatmap__cell--4 {
  background: #15803d;
}

.profile-heatmap__legend {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: var(--space-8);
  margin-top: var(--space-12);
  color: var(--color-text-secondary);
  font-size: 13px;
}

.profile-heatmap__legend .profile-heatmap__cell {
  width: 14px;
  min-width: 14px;
}

.profile-actions {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: var(--space-12);
}

.profile-actions .el-button {
  width: 100%;
  margin-left: 0;
}

.profile-settings__grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--space-16);
}

.profile-setting-card--danger {
  border-color: rgba(239, 68, 68, 0.24);
}

@media (max-width: 767px) {
  .profile-overview,
  .profile-nav,
  .profile-panel,
  .profile-setting-card {
    padding: var(--space-16);
  }

  .profile-overview__identity {
    align-items: flex-start;
  }

  .profile-overview__stats,
  .profile-overview-grid,
  .profile-summary-grid,
  .profile-metric-list,
  .profile-actions,
  .profile-settings__grid {
    grid-template-columns: minmax(0, 1fr);
  }

  .profile-nav {
    flex-direction: column;
  }

  .profile-panel__header {
    align-items: flex-start;
    flex-direction: column;
  }

  .profile-heatmap__summary {
    grid-template-columns: repeat(4, auto);
    text-align: left;
  }
}
</style>
