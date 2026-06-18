<script setup lang="ts">
import { computed } from 'vue'
import { User } from '@element-plus/icons-vue'
import { useRoute } from 'vue-router'
import AppFooter from './AppFooter.vue'
import AppHeader from './AppHeader.vue'

const route = useRoute()

const pageName = computed(() => {
  const placeholder = route.meta.placeholder
  return typeof placeholder === 'string' ? placeholder : 'Page'
})

const pageSummary = computed(() => {
  const summaries: Record<string, string> = {
    Home: '这里是首页内容区占位，后续接入帖子信息流与推荐内容。',
    CreatePost: '这里是发布入口占位，后续接入帖子创建表单与发布流程。',
    Profile: '这里是用户中心占位，后续接入用户信息、我的帖子和我的评论。',
    MyPosts: '这里将展示当前用户发布的帖子列表。',
    MyComments: '这里将展示当前用户发表的评论列表。',
    Settings: '这里将展示账号设置与偏好配置。',
    PostDetail: '这里将展示帖子详情、互动信息与评论列表。',
    Error: '这里是系统错误占位页面。',
    NotFound: '这里是 404 占位页面。',
  }

  return summaries[pageName.value] || '这里是当前页面的占位内容区域。'
})

const userCard = {
  nickname: '匿名同学',
  userId: '#1024',
  tagline: '用最轻的负担表达真实想法',
}
</script>

<template>
  <div class="app-layout">
    <AppHeader />

    <main class="app-layout__main">
      <div class="app-layout__shell">
        <section class="app-layout__content">
          <header class="page-hero">
            <p class="page-hero__eyebrow">CampusTree</p>
            <h1 class="page-hero__title">{{ pageName }}</h1>
            <p class="page-hero__description">{{ pageSummary }}</p>
          </header>

          <section class="page-placeholder">
            <div class="page-placeholder__meta">
              <span class="page-placeholder__tag">Route</span>
              <span class="page-placeholder__path">{{ route.fullPath }}</span>
            </div>
            <div class="page-placeholder__grid">
              <article class="page-placeholder__panel">
                <h2>页面壳层已就绪</h2>
                <p>
                  顶部导航、Logo 区域、首页入口、发布入口、用户中心入口和移动端底部导航已经接入。
                </p>
              </article>
              <article class="page-placeholder__panel">
                <h2>当前阶段说明</h2>
                <p>本页面仅使用占位数据，不接真实 API，不落具体业务逻辑。</p>
              </article>
            </div>
          </section>
        </section>

        <aside class="app-layout__sidebar" aria-label="用户概览">
          <section class="profile-card">
            <div class="profile-card__avatar">
              <el-icon><User /></el-icon>
            </div>
            <div class="profile-card__content">
              <h2>{{ userCard.nickname }}</h2>
              <p>{{ userCard.userId }}</p>
              <span>{{ userCard.tagline }}</span>
            </div>
          </section>
        </aside>
      </div>
    </main>

    <AppFooter />
  </div>
</template>

<style scoped>
.app-layout {
  min-height: 100vh;
  background:
    radial-gradient(circle at top left, rgba(16, 185, 129, 0.12), transparent 26%),
    radial-gradient(circle at top right, rgba(59, 130, 246, 0.08), transparent 22%),
    linear-gradient(180deg, #f9fafb 0%, #f4faf7 100%);
}

.app-layout__main {
  padding: var(--space-24) var(--space-16) calc(88px + env(safe-area-inset-bottom));
}

.app-layout__shell {
  display: grid;
  grid-template-columns: minmax(0, 720px) 280px;
  gap: var(--space-24);
  width: min(100%, 1048px);
  margin: 0 auto;
}

.app-layout__content {
  min-width: 0;
}

.page-hero {
  padding: var(--space-24);
  margin-bottom: var(--space-24);
  border: 1px solid rgba(229, 231, 235, 0.72);
  border-radius: var(--radius-16);
  background: rgba(255, 255, 255, 0.82);
  box-shadow: var(--shadow-card);
}

.page-hero__eyebrow {
  margin-bottom: var(--space-8);
  color: var(--color-primary);
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.page-hero__title {
  margin-bottom: var(--space-12);
  color: var(--color-text-primary);
  font-size: 32px;
  line-height: 1.25;
}

.page-hero__description {
  max-width: 58ch;
  color: var(--color-text-secondary);
  font-size: 16px;
  line-height: 1.75;
}

.page-placeholder {
  padding: var(--space-24);
  border: 1px solid rgba(229, 231, 235, 0.72);
  border-radius: var(--radius-16);
  background: rgba(255, 255, 255, 0.92);
  box-shadow: var(--shadow-card);
}

.page-placeholder__meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--space-8);
  margin-bottom: var(--space-24);
}

.page-placeholder__tag {
  display: inline-flex;
  align-items: center;
  min-height: 24px;
  padding: 0 var(--space-8);
  border-radius: 999px;
  color: var(--color-primary);
  font-size: 13px;
  font-weight: 600;
  background: rgba(16, 185, 129, 0.1);
}

.page-placeholder__path {
  color: var(--color-text-secondary);
  font-size: 13px;
}

.page-placeholder__grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--space-16);
}

.page-placeholder__panel {
  padding: var(--space-16);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-12);
  background: linear-gradient(180deg, #ffffff 0%, #f8fcfa 100%);
}

.page-placeholder__panel h2 {
  margin-bottom: var(--space-8);
  color: var(--color-text-primary);
  font-size: 18px;
  font-weight: 600;
  line-height: 1.5;
}

.page-placeholder__panel p {
  color: var(--color-text-secondary);
  font-size: 16px;
  line-height: 1.75;
}

.app-layout__sidebar {
  position: sticky;
  top: 84px;
  align-self: start;
}

.profile-card {
  padding: var(--space-24);
  border: 1px solid rgba(229, 231, 235, 0.72);
  border-radius: var(--radius-16);
  background: rgba(255, 255, 255, 0.92);
  box-shadow: var(--shadow-card);
}

.profile-card__avatar {
  display: grid;
  place-items: center;
  width: 56px;
  height: 56px;
  margin-bottom: var(--space-16);
  border-radius: 20px;
  color: #ffffff;
  font-size: 28px;
  background: linear-gradient(135deg, #10b981 0%, #3b82f6 100%);
}

.profile-card__content h2 {
  margin-bottom: var(--space-4);
  color: var(--color-text-primary);
  font-size: 18px;
  font-weight: 600;
  line-height: 1.5;
}

.profile-card__content p {
  margin-bottom: var(--space-8);
  color: var(--color-text-secondary);
  font-size: 13px;
}

.profile-card__content span {
  color: var(--color-text-secondary);
  font-size: 14px;
  line-height: 1.6;
}

@media (max-width: 1023px) {
  .app-layout__shell {
    grid-template-columns: minmax(0, 1fr);
  }

  .app-layout__sidebar {
    display: none;
  }
}

@media (max-width: 767px) {
  .app-layout__main {
    padding: var(--space-16) var(--space-16) calc(104px + env(safe-area-inset-bottom));
  }

  .page-hero,
  .page-placeholder {
    padding: var(--space-16);
  }

  .page-hero__title {
    font-size: 24px;
  }

  .page-placeholder__grid {
    grid-template-columns: minmax(0, 1fr);
  }
}
</style>
