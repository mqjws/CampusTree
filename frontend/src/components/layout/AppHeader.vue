<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { Setting, House, Plus, User } from '@element-plus/icons-vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/modules/auth'
import { useUserStore } from '@/stores/modules/user'

type NavItem = {
  label: string
  to: string
  icon: typeof House
  variant: 'text' | 'primary'
}

const route = useRoute()
const authStore = useAuthStore()
const userStore = useUserStore()

const navItems = computed<NavItem[]>(() => [
  {
    label: '首页',
    to: '/home',
    icon: House,
    variant: 'text',
  },
  {
    label: '发布',
    to: '/create',
    icon: Plus,
    variant: 'primary',
  },
  {
    label: authStore.isAuthenticated ? '我的' : '登录',
    to: authStore.isAuthenticated ? '/profile' : '/login',
    icon: User,
    variant: 'text',
  },
])

const isAdmin = computed(() => userStore.currentUser?.role === 'admin')

const activePath = computed(() => route.path)

onMounted(() => {
  if (authStore.isAuthenticated) {
    userStore.fetchCurrentUser().catch(() => undefined)
  }
})
</script>

<template>
  <header class="app-header">
    <div class="app-header__inner">
      <RouterLink class="app-header__brand" to="/home" aria-label="CampusTree 首页">
        <span class="app-header__logo-mark">CT</span>
        <span class="app-header__brand-text">
          <strong>CampusTree</strong>
          <small>匿名校园树洞</small>
        </span>
      </RouterLink>

      <nav class="app-header__nav" aria-label="主导航">
        <RouterLink
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="app-header__link"
          :class="[
            item.variant === 'primary' ? 'app-header__link--primary' : 'app-header__link--text',
            activePath === item.to ? 'is-active' : '',
          ]"
        >
          <el-icon class="app-header__link-icon"><component :is="item.icon" /></el-icon>
          <span>{{ item.label }}</span>
        </RouterLink>
        <RouterLink
          v-if="isAdmin"
          :to="'/admin'"
          class="app-header__link app-header__link--text"
          :class="{ 'is-active': activePath.startsWith('/admin') }"
        >
          <el-icon class="app-header__link-icon"><component :is="Setting" /></el-icon>
          <span>管理</span>
        </RouterLink>
        <a
          class="app-header__intro-link"
          href="https://info.campustreex.com"
          target="_blank"
          rel="noopener noreferrer"
        >
          项目介绍
        </a>
      </nav>
    </div>
  </header>
</template>

<style scoped>
.app-header {
  position: sticky;
  top: 0;
  z-index: 40;
  border-bottom: 1px solid rgba(229, 231, 235, 0.88);
  background: rgba(249, 250, 251, 0.9);
  backdrop-filter: blur(18px);
}

.app-header__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-16);
  width: min(100%, 1200px);
  min-height: 60px;
  margin: 0 auto;
  padding: 0 var(--space-16);
}

.app-header__brand {
  display: inline-flex;
  align-items: center;
  gap: var(--space-12);
  min-width: 0;
}

.app-header__logo-mark {
  display: grid;
  place-items: center;
  width: 40px;
  height: 40px;
  border-radius: 14px;
  color: #ffffff;
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 0.06em;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  box-shadow: 0 10px 24px rgba(16, 185, 129, 0.24);
}

.app-header__brand-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
  color: var(--color-text-primary);
  line-height: 1.1;
}

.app-header__brand-text strong {
  font-size: 18px;
  font-weight: 700;
}

.app-header__brand-text small {
  color: var(--color-text-secondary);
  font-size: 12px;
}

.app-header__nav {
  display: flex;
  align-items: center;
  gap: var(--space-8);
}

.app-header__link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-8);
  min-height: 40px;
  padding: 0 var(--space-16);
  border-radius: var(--radius-8);
  font-size: 14px;
  font-weight: 500;
  transition:
    background-color 200ms ease,
    color 200ms ease,
    transform 120ms ease,
    box-shadow 200ms ease;
}

.app-header__link:hover {
  transform: translateY(-1px);
}

.app-header__link:active {
  transform: scale(0.98);
}

.app-header__link-icon {
  font-size: 18px;
}

.app-header__link--text {
  color: var(--color-text-secondary);
}

.app-header__link--text:hover,
.app-header__link--text.is-active {
  color: var(--color-text-primary);
  background: var(--color-bg-hover);
}

.app-header__link--primary {
  color: #ffffff;
  background: var(--color-primary);
  box-shadow: 0 8px 20px rgba(16, 185, 129, 0.2);
}

.app-header__link--primary:hover,
.app-header__link--primary.is-active {
  background: #059669;
}

.app-header__intro-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 40px;
  padding: 0 var(--space-16);
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: var(--radius-8);
  color: var(--color-primary);
  font-size: 14px;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.72);
  transition:
    color 200ms ease,
    border-color 200ms ease,
    background-color 200ms ease,
    transform 120ms ease,
    box-shadow 200ms ease;
}

.app-header__intro-link:hover,
.app-header__intro-link:focus-visible {
  color: #059669;
  border-color: rgba(5, 150, 105, 0.48);
  background: #ffffff;
  box-shadow: 0 8px 20px rgba(16, 185, 129, 0.14);
  transform: translateY(-1px);
}

@media (max-width: 767px) {
  .app-header__inner {
    min-height: 56px;
  }

  .app-header__brand-text small {
    display: none;
  }

  .app-header__nav {
    gap: 0;
  }

  .app-header__link--text {
    display: none;
  }

  .app-header__link--primary {
    min-height: 44px;
    padding: 0 var(--space-12);
  }

  .app-header__link--primary span {
    display: none;
  }

  .app-header__intro-link {
    min-height: 36px;
    padding: 0 var(--space-12);
    font-size: 13px;
  }
}

@media (max-width: 359px) {
  .app-header__brand {
    gap: var(--space-8);
  }

  .app-header__brand-text strong {
    font-size: 16px;
  }

  .app-header__intro-link {
    padding: 0 var(--space-8);
  }
}
</style>
