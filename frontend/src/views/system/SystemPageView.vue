<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AppLayout from '@/components/layout/AppLayout.vue'

const route = useRoute()

const pageName = computed(() => {
  const placeholder = route.meta.placeholder
  return typeof placeholder === 'string' ? placeholder : 'System'
})

const pageSummary = computed(() => {
  const summaries: Record<string, string> = {
    Error: '这里是系统错误占位页面，后续会接入真实异常页与重试逻辑。',
    NotFound: '这里是 404 占位页面，后续会接入更完整的空状态引导。',
  }

  return summaries[pageName.value] || '当前页面仍处于占位阶段。'
})
</script>

<template>
  <AppLayout :title="pageName" :description="pageSummary" :show-sidebar="false">
    <section class="system-panel">
      <p class="system-panel__eyebrow">Route</p>
      <h2>{{ route.fullPath }}</h2>
      <p>该页面暂未进入业务开发阶段，当前只保留系统级占位内容。</p>
    </section>
  </AppLayout>
</template>

<style scoped>
.system-panel {
  padding: var(--space-24);
  border: 1px solid rgba(229, 231, 235, 0.76);
  border-radius: var(--radius-16);
  background: rgba(255, 255, 255, 0.94);
  box-shadow: var(--shadow-card);
}

.system-panel__eyebrow {
  margin-bottom: var(--space-8);
  color: var(--color-primary);
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.system-panel h2 {
  margin-bottom: var(--space-12);
  color: var(--color-text-primary);
  font-size: 24px;
  line-height: 1.33;
}

.system-panel p {
  color: var(--color-text-secondary);
  font-size: 16px;
  line-height: 1.75;
}
</style>
