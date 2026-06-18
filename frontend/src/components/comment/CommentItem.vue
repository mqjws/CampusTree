<script setup lang="ts">
import { ChatDotRound, Clock, Pointer } from '@element-plus/icons-vue'
import type { CommentRecord } from '@/types/content'

defineProps<{
  comment: CommentRecord
}>()
</script>

<template>
  <article class="comment-item">
    <header class="comment-item__header">
      <div class="comment-item__author">
        <span class="comment-item__avatar">{{ comment.author.avatarEmoji }}</span>
        <div>
          <p class="comment-item__name">{{ comment.author.alias }}</p>
          <p class="comment-item__time">
            <el-icon><Clock /></el-icon>
            <span>{{ comment.relativeTime }}</span>
          </p>
        </div>
      </div>

      <span class="comment-item__likes">
        <el-icon><Pointer /></el-icon>
        {{ comment.likeCount }}
      </span>
    </header>

    <p class="comment-item__content">{{ comment.content }}</p>

    <footer class="comment-item__footer">
      <span>
        <el-icon><ChatDotRound /></el-icon>
        评论占位模式
      </span>
    </footer>
  </article>
</template>

<style scoped>
.comment-item {
  display: grid;
  gap: var(--space-12);
  padding: var(--space-12);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-8);
  background: var(--color-bg-card);
}

.comment-item__header,
.comment-item__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-12);
}

.comment-item__author {
  display: flex;
  align-items: center;
  gap: var(--space-12);
}

.comment-item__avatar {
  display: grid;
  place-items: center;
  width: 36px;
  height: 36px;
  border-radius: 12px;
  background: rgba(16, 185, 129, 0.12);
  font-size: 18px;
}

.comment-item__name {
  margin-bottom: var(--space-4);
  color: var(--color-text-primary);
  font-size: 14px;
  font-weight: 600;
}

.comment-item__time,
.comment-item__likes,
.comment-item__footer {
  display: inline-flex;
  align-items: center;
  gap: var(--space-4);
  color: var(--color-text-secondary);
  font-size: 13px;
}

.comment-item__content {
  color: var(--color-text-primary);
  font-size: 16px;
  line-height: 1.75;
}

@media (max-width: 767px) {
  .comment-item__content {
    font-size: 14px;
  }
}
</style>
