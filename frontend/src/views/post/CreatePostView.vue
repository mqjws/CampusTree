<script setup lang="ts">
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage, ElMessageBox } from 'element-plus'
import { computed, onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import AppLayout from '@/components/layout/AppLayout.vue'
import { createPostCategories } from '@/mock/community'
import * as topicApi from '@/api/topic'
import { usePostStore } from '@/stores/modules/post'
import { useUserStore } from '@/stores/modules/user'
import type { TopicDto } from '@/types/api'
import { formatFullTime } from '@/utils/format'

interface CreatePostForm {
  title: string
  category: string
  topicName: string
  content: string
  allowComments: boolean
}

interface PostDraft {
  title: string
  category: string
  topicName: string
  content: string
  allowComments: boolean
  savedAt: string
}

const DRAFT_KEY_PREFIX = 'campus_tree_post_draft'

const postStore = usePostStore()
const userStore = useUserStore()
const router = useRouter()
const formRef = ref<FormInstance>()
const draftSavedAt = ref<string | null>(null)
const topicOptions = ref<TopicDto[]>([])
const loadingTopics = ref(false)

const form = reactive<CreatePostForm>({
  title: '',
  category: createPostCategories[0],
  topicName: '',
  content: '',
  allowComments: true,
})

const draftKey = computed(() => {
  return `${DRAFT_KEY_PREFIX}_${userStore.currentUser?.id || 'anonymous'}`
})

const draftSavedText = computed(() => {
  return draftSavedAt.value ? formatFullTime(draftSavedAt.value) : ''
})

const rules: FormRules<CreatePostForm> = {
  title: [
    { required: true, message: '请输入标题', trigger: 'blur' },
    { min: 2, max: 60, message: '标题长度为 2 到 60 个字符', trigger: 'blur' },
  ],
  category: [{ required: true, message: '请选择分类', trigger: 'change' }],
  content: [
    { required: true, message: '请输入正文', trigger: 'blur' },
    { min: 10, message: '正文至少输入 10 个字符', trigger: 'blur' },
  ],
}

onMounted(() => {
  fetchTopicOptions()

  const draft = readDraft()

  if (!draft || !hasDraftContent(draft)) {
    return
  }

  draftSavedAt.value = draft.savedAt

  ElMessageBox.confirm(
    `发现一份保存于 ${formatFullTime(draft.savedAt)} 的草稿，是否继续编辑？`,
    '恢复草稿',
    {
      type: 'info',
      confirmButtonText: '继续编辑',
      cancelButtonText: '丢弃草稿',
    },
  )
    .then(() => {
      restoreDraft(draft)
      ElMessage.success('已恢复草稿')
    })
    .catch(() => {
      clearDraft()
      ElMessage.info('已丢弃草稿')
    })
})

function hasDraftContent(draft: Omit<PostDraft, 'savedAt'>): boolean {
  return Boolean(
      draft.title.trim() ||
      draft.content.trim() ||
      draft.topicName.trim() ||
      draft.category !== createPostCategories[0] ||
      draft.allowComments !== true,
  )
}

const defaultTopics = ['生活', '校园', '吐槽', '学习', '美食', '情感', '考研', '就业', '二手', '失物招领']

async function fetchTopicOptions() {
  loadingTopics.value = true

  try {
    const data = await topicApi.listTopics(undefined, 50)
    const existingNames = new Set(data.items.map((t) => t.name))
    const defaults: TopicDto[] = defaultTopics
      .filter((name) => !existingNames.has(name))
      .map((name, i) => ({ id: -(i + 1), name, post_count: 0, created_at: '', updated_at: '' }))
    topicOptions.value = [...defaults, ...data.items]
  } catch {
    topicOptions.value = defaultTopics.map((name, i) => ({ id: -(i + 1), name, post_count: 0, created_at: '', updated_at: '' }))
  } finally {
    loadingTopics.value = false
  }
}

function readDraft(): PostDraft | null {
  const rawDraft = localStorage.getItem(draftKey.value)

  if (!rawDraft) {
    return null
  }

  try {
    const draft = JSON.parse(rawDraft) as PostDraft
    if (
      typeof draft.title !== 'string' ||
      typeof draft.category !== 'string' ||
      typeof draft.content !== 'string' ||
      typeof draft.allowComments !== 'boolean' ||
      typeof draft.savedAt !== 'string'
    ) {
      return null
    }

    return draft
  } catch {
    return null
  }
}

function restoreDraft(draft: PostDraft) {
  form.title = draft.title
  form.category = createPostCategories.includes(draft.category)
    ? draft.category
    : createPostCategories[0]
  form.topicName = draft.topicName
  form.content = draft.content
  form.allowComments = draft.allowComments
  draftSavedAt.value = draft.savedAt
}

function clearDraft() {
  localStorage.removeItem(draftKey.value)
  draftSavedAt.value = null
}

function handleSaveDraft() {
  const draft = {
    title: form.title,
    category: form.category,
    topicName: form.topicName,
    content: form.content,
    allowComments: form.allowComments,
  }

  if (!hasDraftContent(draft)) {
    ElMessage.warning('当前没有可保存的草稿内容')
    return
  }

  const savedAt = new Date().toISOString()
  localStorage.setItem(
    draftKey.value,
    JSON.stringify({
      ...draft,
      savedAt,
    }),
  )
  draftSavedAt.value = savedAt
  ElMessage.success('草稿已保存，下次发布时会提示继续编辑')
}

function handleDiscardDraft() {
  clearDraft()
  ElMessage.success('草稿已清除')
}

async function handleSubmit() {
  const isValid = await formRef.value?.validate().catch(() => false)

  if (!isValid) {
    return
  }

  try {
    await postStore.createPost(
      form.title,
      form.content,
      form.category,
      form.allowComments,
      form.topicName,
    )
    clearDraft()
    ElMessage.success('帖子创建成功')
    await router.push('/')
  } catch (err: any) {
    const msg = err?.response?.data?.message || '帖子创建失败'
    ElMessage.error(msg)
  }
}
</script>

<template>
  <AppLayout
    title="发布一条新内容"
    description="当前页面已接入真实创建帖子接口，UI 结构和设计系统保持不变。"
    :user-card="{
      nickname: userStore.profile.nickname,
      userId: userStore.profile.userId,
      tagline: userStore.profile.tagline,
    }"
  >
    <section class="create-card">
      <el-form ref="formRef" :model="form" :rules="rules" label-position="top" @submit.prevent>
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" maxlength="60" show-word-limit size="large" />
        </el-form-item>

        <el-form-item label="分类" prop="category">
          <el-select v-model="form.category" size="large">
            <el-option
              v-for="category in createPostCategories"
              :key="category"
              :label="category"
              :value="category"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="话题（可选）">
          <el-select
            v-model="form.topicName"
            filterable
            allow-create
            default-first-option
            clearable
            :loading="loadingTopics"
            placeholder="输入关键词搜索话题，或直接输入新话题名（无需加 #）"
            size="large"
            @visible-change="(visible: boolean) => visible && fetchTopicOptions()"
          >
            <el-option
              v-for="topic in topicOptions"
              :key="topic.id"
              :label="`# ${topic.name}`"
              :value="topic.name"
            >
              <span># {{ topic.name }}</span>
              <small>{{ topic.post_count }} 条</small>
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="正文" prop="content">
          <el-input
            v-model="form.content"
            type="textarea"
            :rows="10"
            maxlength="2000"
            show-word-limit
            resize="none"
          />
        </el-form-item>

        <div class="create-card__options">
          <div>
            <h2>评论开关</h2>
            <p>关闭后，帖子详情页将禁止发布新评论。</p>
          </div>
          <el-switch v-model="form.allowComments" />
        </div>

        <div class="create-card__actions">
          <p v-if="draftSavedAt" class="create-card__draft-status">
            草稿保存于 {{ draftSavedText }}
          </p>
          <el-button v-if="draftSavedAt" size="large" plain @click="handleDiscardDraft">
            丢弃草稿
          </el-button>
          <el-button size="large" @click="handleSaveDraft">保存草稿</el-button>
          <el-button
            type="primary"
            size="large"
            :loading="postStore.creating"
            @click="handleSubmit"
          >
            发布内容
          </el-button>
        </div>
      </el-form>
    </section>
  </AppLayout>
</template>

<style scoped>
.create-card {
  padding: var(--space-24);
  border: 1px solid rgba(229, 231, 235, 0.76);
  border-radius: var(--radius-16);
  background: rgba(255, 255, 255, 0.94);
  box-shadow: var(--shadow-card);
}

.create-card :deep(.el-form-item__label) {
  color: var(--color-text-primary);
  font-weight: 500;
}

.create-card__options {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-16);
  padding: var(--space-16);
  margin-bottom: var(--space-24);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-12);
  background: linear-gradient(180deg, #ffffff 0%, #f8fcfa 100%);
}

.create-card__options h2 {
  margin-bottom: var(--space-8);
  color: var(--color-text-primary);
  font-size: 18px;
  font-weight: 600;
}

.create-card__options p {
  color: var(--color-text-secondary);
  font-size: 14px;
  line-height: 1.7;
}

.create-card__actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: var(--space-12);
}

.create-card__draft-status {
  margin-right: auto;
  color: var(--color-text-secondary);
  font-size: 14px;
}

@media (max-width: 767px) {
  .create-card {
    padding: var(--space-16);
  }

  .create-card__options,
  .create-card__actions {
    flex-direction: column;
    align-items: stretch;
  }

  .create-card__draft-status {
    margin-right: 0;
  }
}
</style>
