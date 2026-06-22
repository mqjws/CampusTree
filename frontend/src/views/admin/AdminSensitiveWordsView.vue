<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Delete, Plus, Search, Warning } from '@element-plus/icons-vue'
import AppLayout from '@/components/layout/AppLayout.vue'
import { useUserStore } from '@/stores/modules/user'
import * as adminApi from '@/api/admin'
import type { SensitiveWordDto } from '@/types/api'

const userStore = useUserStore()
const words = ref<SensitiveWordDto[]>([])
const loading = ref(false)
const adding = ref(false)
const newWord = ref('')
const searchKeyword = ref('')

onMounted(() => {
  userStore.fetchCurrentUser().catch(() => undefined)
  fetchWords()
})

async function fetchWords() {
  loading.value = true
  try {
    const keyword = searchKeyword.value.trim() || undefined
    const data = await adminApi.listSensitiveWords(keyword)
    words.value = data.items
  } catch {
    ElMessage.error('获取敏感词列表失败')
  } finally {
    loading.value = false
  }
}

async function handleAdd() {
  const word = newWord.value.trim()
  if (!word) {
    ElMessage.warning('请输入敏感词')
    return
  }

  adding.value = true
  try {
    await adminApi.createSensitiveWord({ word })
    ElMessage.success(`已添加敏感词：${word}`)
    newWord.value = ''
    await fetchWords()
  } catch {
    ElMessage.error('添加失败，可能该敏感词已存在')
  } finally {
    adding.value = false
  }
}

async function handleDelete(word: SensitiveWordDto) {
  try {
    await ElMessageBox.confirm(`确认删除敏感词「${word.word}」？`, '删除确认', {
      type: 'warning',
      confirmButtonText: '删除',
      cancelButtonText: '取消',
    })
    await adminApi.deleteSensitiveWord(word.id)
    ElMessage.success(`已删除：${word.word}`)
    words.value = words.value.filter((w) => w.id !== word.id)
  } catch {
    // 用户取消或失败
  }
}
</script>

<template>
  <AppLayout
    title="敏感词管理"
    description="管理员可在此添加或删除敏感词。被拦截的内容会在发帖和评论时提示用户。"
    :user-card="{
      nickname: userStore.profile.nickname,
      userId: userStore.profile.userId,
      tagline: userStore.profile.tagline,
    }"
  >
    <section class="admin-card">
      <div class="admin-card__header">
        <h2>
          <el-icon><Warning /></el-icon>
          敏感词列表
        </h2>
        <span class="admin-card__count">共 {{ words.length }} 条</span>
      </div>

      <div class="admin-card__actions">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索敏感词"
          :prefix-icon="Search"
          size="large"
          clearable
          @keyup.enter="fetchWords"
          @clear="fetchWords"
        />
        <div class="admin-card__add">
          <el-input
            v-model="newWord"
            placeholder="输入新敏感词"
            size="large"
            maxlength="50"
            show-word-limit
            @keyup.enter="handleAdd"
          />
          <el-button type="primary" size="large" :loading="adding" :icon="Plus" @click="handleAdd">
            添加
          </el-button>
        </div>
      </div>

      <div v-loading="loading" class="admin-card__body">
        <el-empty v-if="!loading && words.length === 0" description="暂无敏感词" />
        <div v-else class="word-table">
          <div v-for="word in words" :key="word.id" class="word-table__row">
            <span class="word-table__text">{{ word.word }}</span>
            <el-button
              type="danger"
              :icon="Delete"
              size="small"
              plain
              @click="handleDelete(word)"
            >
              删除
            </el-button>
          </div>
        </div>
      </div>
    </section>
  </AppLayout>
</template>

<style scoped>
.admin-card {
  display: grid;
  gap: var(--space-20);
  padding: var(--space-24);
  border: 1px solid rgba(229, 231, 235, 0.76);
  border-radius: var(--radius-16);
  background: rgba(255, 255, 255, 0.94);
  box-shadow: var(--shadow-card);
}

.admin-card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.admin-card__header h2 {
  display: flex;
  align-items: center;
  gap: var(--space-8);
  color: var(--color-text-primary);
  font-size: 20px;
  font-weight: 700;
}

.admin-card__count {
  color: var(--color-text-secondary);
  font-size: 14px;
}

.admin-card__actions {
  display: grid;
  gap: var(--space-12);
}

.admin-card__add {
  display: flex;
  gap: var(--space-12);
}

.admin-card__add .el-input {
  flex: 1;
}

.word-table {
  display: grid;
  gap: var(--space-8);
}

.word-table__row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-12);
  padding: var(--space-12) var(--space-16);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-8);
  background: linear-gradient(180deg, #ffffff 0%, #f8fcfa 100%);
}

.word-table__text {
  color: var(--color-text-primary);
  font-size: 15px;
  font-weight: 500;
}

@media (max-width: 767px) {
  .admin-card {
    padding: var(--space-16);
  }

  .admin-card__add {
    flex-direction: column;
  }
}
</style>
