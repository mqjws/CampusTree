<script setup lang="ts">
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage, ElMessageBox } from 'element-plus'
import { computed, onMounted, reactive, ref } from 'vue'
import { EditPen, MessageBox, Setting, Tickets } from '@element-plus/icons-vue'
import { useRoute, useRouter } from 'vue-router'
import AppLayout from '@/components/layout/AppLayout.vue'
import CommentList from '@/components/comment/CommentList.vue'
import PostCard from '@/components/post/PostCard.vue'
import { useAuthStore } from '@/stores/modules/auth'
import { useUserStore } from '@/stores/modules/user'
import * as userApi from '@/api/user'

interface PasswordForm {
  oldPassword: string
  newPassword: string
  confirmPassword: string
}

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const authStore = useAuthStore()
const passwordFormRef = ref<FormInstance>()
const passwordSubmitting = ref(false)

const passwordForm = reactive<PasswordForm>({
  oldPassword: '',
  newPassword: '',
  confirmPassword: '',
})

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
    overview: '用户基础信息、统计数据、我的帖子和我的评论都已接入真实接口。',
    posts: '这里展示当前登录用户发布的真实帖子列表。',
    comments: '这里展示当前登录用户发表的真实评论列表。',
    settings: '设置页已补齐最小可用功能：修改密码、清理缓存、退出登录。',
  }

  return map[section.value]
})

onMounted(() => {
  userStore.fetchCurrentUser().catch(() => undefined)
  userStore.fetchMyPosts().catch(() => undefined)
  userStore.fetchMyComments().catch(() => undefined)
  userStore.fetchMyStats().catch(() => undefined)
})

function openPost(id: number) {
  router.push(`/post/${id}`)
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
      <article class="profile-panel">
        <h2>当前联调状态</h2>
        <p>用户中心的核心展示数据已切换到真实后端接口。</p>
      </article>
      <el-empty v-if="userStore.myPosts.length === 0" description="当前用户还没有发布帖子" />
      <PostCard
        v-for="post in userStore.myPosts.slice(0, 2)"
        v-else
        :key="post.id"
        :post="post"
        @select="openPost"
      />
    </section>

    <section v-else-if="section === 'posts'" class="profile-panels">
      <el-empty v-if="userStore.myPosts.length === 0" description="当前用户还没有发布帖子" />
      <PostCard
        v-for="post in userStore.myPosts"
        v-else
        :key="post.id"
        :post="post"
        @select="openPost"
      />
    </section>

    <section v-else-if="section === 'comments'" class="profile-panels">
      <CommentList :comments="userStore.myComments" title="我的评论" />
    </section>

    <section v-else class="profile-settings">
      <article class="profile-panel">
        <h2>账号设置</h2>
        <p>当前可直接修改密码、清理缓存并退出登录。</p>
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

.profile-panel h2,
.profile-setting-card h3 {
  margin-bottom: var(--space-8);
  color: var(--color-text-primary);
  font-size: 18px;
  font-weight: 600;
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
  .profile-settings__grid {
    grid-template-columns: minmax(0, 1fr);
  }

  .profile-nav {
    flex-direction: column;
  }
}
</style>
