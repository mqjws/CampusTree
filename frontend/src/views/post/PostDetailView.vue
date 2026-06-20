<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { ArrowLeft, ChatDotRound, Clock, Pointer } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useRoute, useRouter } from 'vue-router'
import AppLayout from '@/components/layout/AppLayout.vue'
import CommentList from '@/components/comment/CommentList.vue'
import { useAuthStore } from '@/stores/modules/auth'
import { useCommentStore } from '@/stores/modules/comment'
import { usePostStore } from '@/stores/modules/post'
import { useUserStore } from '@/stores/modules/user'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const postStore = usePostStore()
const commentStore = useCommentStore()
const userStore = useUserStore()
const commentDraft = ref('')

const postId = computed(() => Number(route.params.id))
const post = computed(() => postStore.currentPost)
const comments = computed(() => commentStore.getComments(postId.value))

async function handleCreateComment() {
  if (!authStore.isAuthenticated) {
    ElMessage.warning('请先登录后再评论')
    await router.push({
      path: '/login',
      query: { redirect: route.fullPath },
    })
    return
  }

  if (!commentDraft.value.trim()) {
    return
  }

  try {
    await commentStore.createComment(postId.value, commentDraft.value.trim())
    postStore.incrementCommentCount(postId.value)
    ElMessage.success('评论已提交')
    commentDraft.value = ''
  } catch {
    ElMessage.error('评论提交失败')
  }
}

onMounted(() => {
  postStore.fetchPostDetail(postId.value).catch(() => undefined)
  commentStore.fetchComments(postId.value).catch(() => undefined)
  userStore.fetchCurrentUser().catch(() => undefined)
})
</script>

<template>
  <AppLayout
    title="帖子详情"
    :description="post?.summary || '正在加载帖子详情...'"
    :user-card="{
      nickname: userStore.profile.nickname,
      userId: userStore.profile.userId,
      tagline: userStore.profile.tagline,
    }"
  >
    <section v-loading="postStore.loading" class="detail-card">
      <template v-if="post">
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
      </template>
    </section>

    <section class="detail-comment-box">
      <div class="detail-comment-box__header">
        <h2>发表评论</h2>
        <p>当前输入区已接入真实创建评论接口。</p>
      </div>

      <el-input
        v-model="commentDraft"
        type="textarea"
        :rows="4"
        placeholder="说点什么..."
        resize="none"
      />
      <div class="detail-comment-box__footer">
        <span>{{ commentDraft.length }} / 500</span>
        <el-button
          type="primary"
          size="large"
          :loading="commentStore.creating"
          @click="handleCreateComment"
        >
          发送评论
        </el-button>
      </div>
    </section>

    <CommentList :comments="comments" />
  </AppLayout>
</template>

<style scoped>
.detail-card,
.detail-comment-box {
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
.detail-comment-box__header p {
  color: var(--color-text-secondary);
  font-size: 16px;
  line-height: 1.8;
}

.detail-comment-box {
  display: grid;
  gap: var(--space-16);
}

.detail-comment-box__header h2 {
  margin-bottom: var(--space-8);
  color: var(--color-text-primary);
  font-size: 18px;
  font-weight: 600;
}

@media (max-width: 767px) {
  .detail-card,
  .detail-comment-box {
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
