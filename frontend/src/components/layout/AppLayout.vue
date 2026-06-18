<script setup lang="ts">
import { computed } from 'vue'
import { User } from '@element-plus/icons-vue'
import AppFooter from './AppFooter.vue'
import AppHeader from './AppHeader.vue'

interface SidebarUserCard {
  nickname: string
  userId: string
  tagline: string
}

const props = withDefaults(
  defineProps<{
    title: string
    description: string
    eyebrow?: string
    showSidebar?: boolean
    userCard?: SidebarUserCard
  }>(),
  {
    eyebrow: 'CampusTree',
    showSidebar: true,
    userCard: () => ({
      nickname: '匿名同学',
      userId: '#1024',
      tagline: '用最轻的负担表达真实想法',
    }),
  },
)

const fallbackUserCard = computed(() => props.userCard)
</script>

<template>
  <div class="app-layout">
    <AppHeader />

    <main class="app-layout__main">
      <div class="app-layout__shell" :class="{ 'app-layout__shell--single': !showSidebar }">
        <section class="app-layout__content">
          <header class="page-hero">
            <p class="page-hero__eyebrow">{{ eyebrow }}</p>
            <h1 class="page-hero__title">{{ title }}</h1>
            <p class="page-hero__description">{{ description }}</p>
          </header>

          <section class="page-content">
            <slot />
          </section>
        </section>

        <aside v-if="showSidebar" class="app-layout__sidebar" aria-label="页面辅助信息">
          <slot name="sidebar">
            <section class="profile-card">
              <div class="profile-card__avatar">
                <el-icon><User /></el-icon>
              </div>
              <div class="profile-card__content">
                <h2>{{ fallbackUserCard.nickname }}</h2>
                <p>{{ fallbackUserCard.userId }}</p>
                <span>{{ fallbackUserCard.tagline }}</span>
              </div>
            </section>
          </slot>
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

.app-layout__shell--single {
  grid-template-columns: minmax(0, 820px);
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

.page-content {
  display: grid;
  gap: var(--space-24);
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
  .app-layout__shell,
  .app-layout__shell--single {
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

  .page-hero {
    padding: var(--space-16);
  }

  .page-hero__title {
    font-size: 24px;
  }
}
</style>
