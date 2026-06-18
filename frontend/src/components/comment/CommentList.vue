<script setup lang="ts">
import CommentItem from './CommentItem.vue'
import type { CommentRecord } from '@/types/content'

defineProps<{
  comments: CommentRecord[]
  title?: string
}>()
</script>

<template>
  <section class="comment-list">
    <header class="comment-list__header">
      <h2>{{ title || `评论 (${comments.length})` }}</h2>
      <p>当前为占位评论列表，后续接入真实评论接口。</p>
    </header>

    <div class="comment-list__items">
      <CommentItem v-for="comment in comments" :key="comment.id" :comment="comment" />
    </div>
  </section>
</template>

<style scoped>
.comment-list {
  display: grid;
  gap: var(--space-16);
}

.comment-list__header h2 {
  margin-bottom: var(--space-8);
  color: var(--color-text-primary);
  font-size: 18px;
  font-weight: 600;
}

.comment-list__header p {
  color: var(--color-text-secondary);
  font-size: 14px;
  line-height: 1.7;
}

.comment-list__items {
  display: grid;
  gap: var(--space-12);
}
</style>
