<script setup lang="ts">
import { ChatDotRound, Clock, Pointer, View } from '@element-plus/icons-vue'
import type { PostRecord } from '@/types/content'

defineProps<{
  post: PostRecord
}>()

const emit = defineEmits<{
  select: [id: number]
}>()

function handleSelect(id: number) {
  emit('select', id)
}
</script>

<template>
  <article class="post-card" @click="handleSelect(post.id)">
    <header class="post-card__header">
      <div class="post-card__author">
        <span class="post-card__avatar">{{ post.author.avatarEmoji }}</span>
        <div>
          <p class="post-card__author-name">{{ post.author.alias }}</p>
          <p class="post-card__time">
            <el-icon><Clock /></el-icon>
            <span>{{ post.relativeTime }}</span>
          </p>
        </div>
      </div>

      <el-tag effect="plain" round>{{ post.category }}</el-tag>
    </header>

    <div class="post-card__body">
      <h3 class="post-card__title">{{ post.title }}</h3>
      <p class="post-card__summary">{{ post.summary }}</p>
    </div>

    <footer class="post-card__footer">
      <div class="post-card__stats">
        <span>
          <el-icon><Pointer /></el-icon>
          {{ post.likeCount }}
        </span>
        <span>
          <el-icon><ChatDotRound /></el-icon>
          {{ post.commentCount }}
        </span>
      </div>

      <span class="post-card__detail">
        <span>查看详情</span>
        <el-icon><View /></el-icon>
      </span>
    </footer>
  </article>
</template>

<style scoped>
.post-card {
  display: grid;
  gap: var(--space-16);
  padding: var(--space-16);
  border: 1px solid rgba(229, 231, 235, 0.76);
  border-radius: var(--radius-12);
  background: var(--color-bg-card);
  box-shadow: var(--shadow-card);
  cursor: pointer;
  transition:
    transform 200ms ease,
    box-shadow 200ms ease,
    border-color 200ms ease;
}

.post-card:hover {
  border-color: rgba(16, 185, 129, 0.22);
  box-shadow: var(--shadow-hover);
  transform: translateY(-2px);
}

.post-card__header,
.post-card__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-12);
}

.post-card__author {
  display: flex;
  align-items: center;
  gap: var(--space-12);
}

.post-card__avatar {
  display: grid;
  place-items: center;
  width: 40px;
  height: 40px;
  border-radius: 14px;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.14), rgba(59, 130, 246, 0.12));
  font-size: 20px;
}

.post-card__author-name {
  margin-bottom: var(--space-4);
  color: var(--color-text-primary);
  font-size: 14px;
  font-weight: 600;
}

.post-card__time {
  display: inline-flex;
  align-items: center;
  gap: var(--space-4);
  color: var(--color-text-secondary);
  font-size: 13px;
}

.post-card__body {
  display: grid;
  gap: var(--space-8);
}

.post-card__title {
  color: var(--color-text-primary);
  font-size: 18px;
  font-weight: 600;
  line-height: 1.5;
}

.post-card__summary {
  color: var(--color-text-secondary);
  font-size: 16px;
  line-height: 1.75;
}

.post-card__stats,
.post-card__detail {
  display: inline-flex;
  align-items: center;
  gap: var(--space-12);
  color: var(--color-text-secondary);
  font-size: 13px;
}

.post-card__stats span,
.post-card__detail {
  display: inline-flex;
  align-items: center;
  gap: var(--space-4);
}

.post-card__detail {
  color: var(--color-primary);
  font-weight: 500;
}

@media (max-width: 767px) {
  .post-card__title {
    font-size: 16px;
  }

  .post-card__summary {
    font-size: 14px;
  }
}
</style>
