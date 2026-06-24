<script setup lang="ts">
import { computed } from 'vue'
import { House, RefreshRight } from '@element-plus/icons-vue'
import { useRoute, useRouter } from 'vue-router'
import AppLayout from '@/components/layout/AppLayout.vue'

const route = useRoute()
const router = useRouter()

const pageName = computed(() => {
  const placeholder = route.meta.placeholder
  return typeof placeholder === 'string' ? placeholder : 'System'
})

const isNotFound = computed(() => pageName.value === 'NotFound')

const pageTitle = computed(() => (isNotFound.value ? '页面不存在' : '系统暂时不可用'))

const pageSummary = computed(() => {
  const summaries: Record<string, string> = {
    Error: '当前页面遇到异常，请稍后重试或返回首页继续浏览。',
    NotFound: '你访问的地址不存在，可能是链接已失效，也可能是路径输入有误。',
  }

  return summaries[pageName.value] || '当前页面暂时不可用，请返回首页继续浏览。'
})

function goHome() {
  router.push('/home')
}

function goBack() {
  if (window.history.length > 1) {
    router.back()
    return
  }

  goHome()
}
</script>

<template>
  <AppLayout :title="pageTitle" :description="pageSummary" :show-sidebar="false">
    <section class="system-panel">
      <p class="system-panel__eyebrow">{{ isNotFound ? '404' : 'Error' }}</p>
      <h2>{{ isNotFound ? '没有找到这个页面' : '页面加载失败' }}</h2>
      <p>
        当前访问路径：
        <code>{{ route.fullPath }}</code>
      </p>
      <div class="system-panel__actions">
        <el-button type="primary" size="large" @click="goHome">
          <el-icon><House /></el-icon>
          返回首页
        </el-button>
        <el-button plain size="large" @click="goBack">
          <el-icon><RefreshRight /></el-icon>
          返回上一页
        </el-button>
      </div>
    </section>
  </AppLayout>
</template>

<style scoped>
.system-panel {
  display: grid;
  gap: var(--space-16);
  padding: var(--space-24);
  border: 1px solid rgba(229, 231, 235, 0.76);
  border-radius: var(--radius-16);
  background: rgba(255, 255, 255, 0.94);
  box-shadow: var(--shadow-card);
}

.system-panel__eyebrow {
  color: var(--color-primary);
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.system-panel h2 {
  color: var(--color-text-primary);
  font-size: 24px;
  line-height: 1.33;
}

.system-panel p {
  color: var(--color-text-secondary);
  font-size: 16px;
  line-height: 1.75;
}

.system-panel code {
  padding: 2px 6px;
  border-radius: var(--radius-4);
  color: var(--color-text-primary);
  font-size: 14px;
  background: var(--color-bg-hover);
  overflow-wrap: anywhere;
}

.system-panel__actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-12);
}

@media (max-width: 767px) {
  .system-panel {
    padding: var(--space-16);
  }

  .system-panel__actions {
    flex-direction: column;
  }
}
</style>
