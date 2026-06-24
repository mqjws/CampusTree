<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import {
  ArrowLeft,
  ChatDotRound,
  Clock,
  Delete,
  Pointer,
  View,
  Warning,
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRoute, useRouter } from 'vue-router'
import AppLayout from '@/components/layout/AppLayout.vue'
import CommentList from '@/components/comment/CommentList.vue'
import * as postApi from '@/api/post'
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
const reportDialogVisible = ref(false)
const reportSubmitting = ref(false)

const reportReasons = ['违法违规', '辱骂攻击', '广告营销', '色情低俗', '其他']
const reportForm = reactive({
  reason: reportReasons[0],
  description: '',
})

type ApiError = {
  response?: {
    status?: number
    data?: {
      message?: string
    }
  }
}

const postId = computed(() => Number(route.params.id))
const post = computed(() => postStore.currentPost)
const comments = computed(() => commentStore.getComments(postId.value))
const contentParagraphs = computed(() => {
  return post.value?.content.split('\n\n').filter((paragraph) => paragraph.trim()) || []
})
const isAuthor = computed(() => {
  return Boolean(
    authStore.isAuthenticated &&
    post.value &&
    userStore.currentUser &&
    post.value.author.id === userStore.currentUser.id,
  )
})

function getApiError(err: unknown): ApiError | null {
  if (typeof err !== 'object' || err === null || !('response' in err)) {
    return null
  }

  return err as ApiError
}

function getApiErrorMessage(err: unknown, fallback: string) {
  return getApiError(err)?.response?.data?.message || fallback
}

async function handleCreateComment() {
  if (post.value && !post.value.allowComments) {
    ElMessage.warning('该帖子已关闭评论')
    return
  }

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
  } catch (err: unknown) {
    ElMessage.error(getApiErrorMessage(err, '评论提交失败'))
  }
}

async function handleToggleLikePost() {
  if (!authStore.isAuthenticated) {
    ElMessage.warning('请先登录后再点赞')
    await router.push({
      path: '/login',
      query: { redirect: route.fullPath },
    })
    return
  }

  if (!post.value) {
    return
  }

  try {
    if (post.value.likedByCurrentUser) {
      await postStore.unlike(postId.value)
      ElMessage.success('已取消点赞')
      return
    }

    await postStore.like(postId.value)
    ElMessage.success('点赞成功')
  } catch {
    ElMessage.error('点赞状态更新失败')
  }
}

async function handleDeletePost() {
  if (!post.value) {
    return
  }

  try {
    await ElMessageBox.confirm(`确认删除帖子「${post.value.title}」？`, '删除确认', {
      type: 'warning',
      confirmButtonText: '删除',
      cancelButtonText: '取消',
    })
    await postStore.deletePost(postId.value)
    ElMessage.success('帖子已删除')
    await router.push('/home')
  } catch {
    // 用户取消或删除失败
  }
}

async function handleOpenReport() {
  if (!authStore.isAuthenticated) {
    ElMessage.warning('请先登录后再举报')
    await router.push({
      path: '/login',
      query: { redirect: route.fullPath },
    })
    return
  }

  reportForm.reason = reportReasons[0]
  reportForm.description = ''
  reportDialogVisible.value = true
}

async function handleSubmitReport() {
  if (!post.value || !reportForm.reason) {
    return
  }

  reportSubmitting.value = true
  try {
    await postApi.reportPost(postId.value, {
      reason: reportForm.reason,
      description: reportForm.description.trim(),
    })
    reportDialogVisible.value = false
    ElMessage.success('举报已提交，管理员会在后台查看')
  } catch (err: unknown) {
    ElMessage.error(getApiErrorMessage(err, '举报提交失败'))
  } finally {
    reportSubmitting.value = false
  }
}

async function fetchDetail() {
  try {
    await postStore.fetchPostDetail(postId.value)
    await commentStore.fetchComments(postId.value).catch(() => undefined)
  } catch (err: unknown) {
    if (getApiError(err)?.response?.status === 401) {
      ElMessage.warning('该帖子仅注册用户可见，请先登录')
      await router.push({
        path: '/login',
        query: { redirect: route.fullPath },
      })
    }
  }
}

onMounted(() => {
  fetchDetail()
  if (authStore.isAuthenticated) {
    userStore.fetchCurrentUser().catch(() => undefined)
  }
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
          <el-button plain size="large" @click="router.push('/home')">
            <el-icon><ArrowLeft /></el-icon>
            返回首页
          </el-button>
          <div class="detail-card__action-group">
            <el-tag v-if="post.registeredOnly" effect="plain" round>注册用户可见</el-tag>
            <el-tag effect="plain" round>{{ post.category }}</el-tag>
            <el-button plain size="large" @click="handleOpenReport">
              <el-icon><Warning /></el-icon>
              举报
            </el-button>
            <el-button v-if="isAuthor" type="danger" plain size="large" @click="handleDeletePost">
              <el-icon><Delete /></el-icon>
              删除
            </el-button>
          </div>
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
          <p v-if="!post.content.trim()" class="detail-card__empty">暂无正文</p>
          <template v-else>
            <p v-for="paragraph in contentParagraphs" :key="paragraph">{{ paragraph }}</p>
          </template>
        </div>

        <div class="detail-card__stats">
          <span>
            <el-icon><View /></el-icon>
            {{ post.viewCount }} 浏览
          </span>
          <el-button
            :type="post.likedByCurrentUser ? 'primary' : 'default'"
            :plain="!post.likedByCurrentUser"
            size="small"
            @click="handleToggleLikePost"
          >
            <el-icon><Pointer /></el-icon>
            {{ post.likedByCurrentUser ? '已点赞' : '点赞' }} {{ post.likeCount }}
          </el-button>
          <span>
            <el-icon><ChatDotRound /></el-icon>
            {{ post.commentCount }} 评论
          </span>
        </div>
      </template>
    </section>

    <section v-if="post?.allowComments" class="detail-comment-box">
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

    <section v-else-if="post" class="detail-comment-box detail-comment-box--disabled">
      <div class="detail-comment-box__header">
        <h2>评论已关闭</h2>
        <p>该帖子不接受新评论，已有评论仍会显示在下方。</p>
      </div>
    </section>

    <CommentList :comments="comments" />

    <el-dialog v-model="reportDialogVisible" title="举报帖子" width="420px">
      <el-form label-position="top">
        <el-form-item label="举报理由">
          <el-select v-model="reportForm.reason" size="large">
            <el-option
              v-for="reason in reportReasons"
              :key="reason"
              :label="reason"
              :value="reason"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="补充说明">
          <el-input
            v-model="reportForm.description"
            type="textarea"
            :rows="4"
            maxlength="500"
            show-word-limit
            resize="none"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="reportDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="reportSubmitting" @click="handleSubmitReport">
          提交举报
        </el-button>
      </template>
    </el-dialog>
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

.detail-card__action-group {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: flex-end;
  gap: var(--space-8);
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

.detail-card__empty {
  color: var(--color-text-disabled);
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

  .detail-card__action-group {
    justify-content: flex-start;
  }

  .detail-card__title {
    font-size: 20px;
  }
}
</style>
