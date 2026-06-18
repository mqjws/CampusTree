<script setup lang="ts">
import { computed } from 'vue'
import { ArrowLeft, ChatDotRound, Clock, Pointer } from '@element-plus/icons-vue'
import { useRoute, useRouter } from 'vue-router'
import AppLayout from '@/components/layout/AppLayout.vue'
import CommentList from '@/components/comment/CommentList.vue'
import { getCommentsByPostId, getPostById, mockProfile } from '@/mock/community'

const route = useRoute()
const router = useRouter()

const postId = computed(() => Number(route.params.id))
const post = computed(() => getPostById(postId.value) || getPostById(1))
const comments = computed(() => getCommentsByPostId(postId.value))
</script>

<template>
  <AppLayout
    v-if="post"
    title="帖子详情"
    :description="post.summary"
    :user-card="{
      nickname: mockProfile.nickname,
      userId: mockProfile.userId,
      tagline: mockProfile.tagline,
    }"
  >
    <section class="detail-card">
      <div class="detail-card__actions">
        <el-button plain size="large" @click="router.push('/')">
          <el-icon><ArrowLeft /></el-icon>
          返回首页
        </el-button>
        <el-tag effect="plain" round>{{ post.category }}</el-tag>
      </div>

      <div class="detail-card__meta">
        <span class="detail-card__avatar">{{ post.author.avatarEmoji }}</span>
        <div>
          <p class="detail-card__name">{{ post.author.alias }}</p>
          <p class="detail-card__time">
            <el-icon><Clock /></el-icon>
            <span>{{ post.fullTime }}</span>
          </p>
        </div>
      </div>

      <h2 class="detail-card__title">{{ post.title }}</h2>
      <div class="detail-card__content">
        <p v-for="paragraph in post.content.split('\n\n')" :key="paragraph">{{ paragraph }}</p>
      </div>

      <div class="detail-card__stats">
        <span>
          <el-icon><Pointer /></el-icon>
          {{ post.likeCount }} 点赞
        </span>
        <span>
          <el-icon><ChatDotRound /></el-icon>
          {{ post.commentCount }} 评论
        </span>
      </div>
    </section>

    <section class="detail-comment-box">
      <div class="detail-comment-box__header">
        <h2>发表评论</h2>
        <p>当前为占位输入区，后续接入创建评论接口。</p>
      </div>

      <el-input
        type="textarea"
        :rows="4"
        placeholder="说点什么……当前不会提交到服务器。"
        resize="none"
      />
      <div class="detail-comment-box__footer">
        <span>0 / 500</span>
        <el-button type="primary" size="large">发送评论</el-button>
      </div>
    </section>

    <CommentList :comments="comments" />

    <template #sidebar>
      <div class="detail-sidebar">
        <section class="sidebar-card">
          <h2>阅读摘要</h2>
          <p>当前详情页已完成内容结构、互动摘要、评论列表和评论输入区布局。</p>
        </section>
        <section class="sidebar-card">
          <h2>作者状态</h2>
          <p>{{ post.author.alias }} · {{ post.relativeTime }}</p>
          <el-button class="sidebar-card__button" plain size="large">查看更多占位内容</el-button>
        </section>
      </div>
    </template>
  </AppLayout>
</template>

<style scoped>
.detail-card,
.detail-comment-box,
.sidebar-card {
  padding: var(--space-24);
  border: 1px solid rgba(229, 231, 235, 0.76);
  border-radius: var(--radius-16);
  background: rgba(255, 255, 255, 0.94);
  box-shadow: var(--shadow-card);
}

.detail-card {
  display: grid;
  gap: var(--space-16);
}

.detail-card__actions,
.detail-card__stats,
.detail-comment-box__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-12);
}

.detail-card__meta {
  display: flex;
  align-items: center;
  gap: var(--space-12);
}

.detail-card__avatar {
  display: grid;
  place-items: center;
  width: 44px;
  height: 44px;
  border-radius: 16px;
  background: rgba(16, 185, 129, 0.12);
  font-size: 22px;
}

.detail-card__name {
  margin-bottom: var(--space-4);
  color: var(--color-text-primary);
  font-size: 14px;
  font-weight: 600;
}

.detail-card__time,
.detail-card__stats span,
.detail-comment-box__footer span {
  display: inline-flex;
  align-items: center;
  gap: var(--space-4);
  color: var(--color-text-secondary);
  font-size: 13px;
}

.detail-card__title {
  color: var(--color-text-primary);
  font-size: 24px;
  font-weight: 700;
  line-height: 1.33;
}

.detail-card__content {
  display: grid;
  gap: var(--space-16);
}

.detail-card__content p,
.detail-comment-box__header p,
.sidebar-card p {
  color: var(--color-text-secondary);
  font-size: 16px;
  line-height: 1.8;
}

.detail-comment-box {
  display: grid;
  gap: var(--space-16);
}

.detail-comment-box__header h2,
.sidebar-card h2 {
  margin-bottom: var(--space-8);
  color: var(--color-text-primary);
  font-size: 18px;
  font-weight: 600;
}

.detail-sidebar {
  display: grid;
  gap: var(--space-16);
}

.sidebar-card__button {
  margin-top: var(--space-16);
  width: 100%;
}

@media (max-width: 767px) {
  .detail-card,
  .detail-comment-box,
  .sidebar-card {
    padding: var(--space-16);
  }

  .detail-card__actions,
  .detail-card__stats,
  .detail-comment-box__footer {
    flex-direction: column;
    align-items: stretch;
  }

  .detail-card__title {
    font-size: 20px;
  }
}
</style>
