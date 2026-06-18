<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { EditPen, MessageBox, Setting, Tickets } from '@element-plus/icons-vue'
import { useRoute, useRouter } from 'vue-router'
import AppLayout from '@/components/layout/AppLayout.vue'
import CommentList from '@/components/comment/CommentList.vue'
import PostCard from '@/components/post/PostCard.vue'
import { useUserStore } from '@/stores/modules/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

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
    settings: '设置页结构保留，等待后续接入账号设置类接口。',
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
        <p>设置页结构保留不变，等待后续接入修改密码、清理缓存等真实接口。</p>
      </article>
      <div class="profile-settings__grid">
        <article class="profile-setting-card">
          <h3>修改密码</h3>
          <p>后端文档中尚未明确提供修改密码接口。</p>
          <el-button plain size="large">待接口补齐</el-button>
        </article>
        <article class="profile-setting-card">
          <h3>清理缓存</h3>
          <p>前端本地可实现，但暂未纳入当前联调范围。</p>
          <el-button plain size="large">保留结构</el-button>
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
