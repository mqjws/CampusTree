<script setup lang="ts">
import { House, Plus, User } from '@element-plus/icons-vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const items = [
  { label: '首页', to: '/home', icon: House },
  { label: '发布', to: '/create', icon: Plus },
  { label: '我的', to: '/profile', icon: User },
]
</script>

<template>
  <nav class="app-footer" aria-label="移动端主导航">
    <RouterLink
      v-for="item in items"
      :key="item.to"
      :to="item.to"
      class="app-footer__item"
      :class="route.path === item.to ? 'is-active' : ''"
    >
      <span class="app-footer__icon-wrap" :class="item.to === '/create' ? 'is-primary' : ''">
        <el-icon class="app-footer__icon"><component :is="item.icon" /></el-icon>
      </span>
      <span class="app-footer__label">{{ item.label }}</span>
    </RouterLink>
  </nav>
</template>

<style scoped>
.app-footer {
  position: fixed;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: 45;
  display: none;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  align-items: center;
  padding: var(--space-8) var(--space-16) calc(var(--space-8) + env(safe-area-inset-bottom));
  border-top: 1px solid rgba(229, 231, 235, 0.9);
  background: rgba(255, 255, 255, 0.94);
  backdrop-filter: blur(18px);
}

.app-footer__item {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-4);
  color: var(--color-text-secondary);
  font-size: 12px;
  font-weight: 500;
}

.app-footer__icon-wrap {
  display: grid;
  place-items: center;
  width: 36px;
  height: 36px;
  border-radius: 12px;
  transition:
    color 200ms ease,
    background-color 200ms ease,
    transform 120ms ease,
    box-shadow 200ms ease;
}

.app-footer__item:active .app-footer__icon-wrap {
  transform: scale(0.96);
}

.app-footer__icon-wrap.is-primary {
  color: #ffffff;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  box-shadow: 0 10px 24px rgba(16, 185, 129, 0.22);
}

.app-footer__icon {
  font-size: 20px;
}

.app-footer__item.is-active {
  color: var(--color-text-primary);
}

.app-footer__item.is-active .app-footer__icon-wrap:not(.is-primary) {
  color: var(--color-primary);
  background: rgba(16, 185, 129, 0.1);
}

@media (max-width: 767px) {
  .app-footer {
    display: grid;
  }
}
</style>
