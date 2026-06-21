<script setup lang="ts">
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import AppLayout from '@/components/layout/AppLayout.vue'
import { createPostCategories } from '@/mock/community'
import { usePostStore } from '@/stores/modules/post'
import { useUserStore } from '@/stores/modules/user'

interface CreatePostForm {
  title: string
  category: string
  content: string
  allowComments: boolean
}

const postStore = usePostStore()
const userStore = useUserStore()
const router = useRouter()
const formRef = ref<FormInstance>()

const form = reactive<CreatePostForm>({
  title: '',
  category: createPostCategories[0],
  content: '',
  allowComments: true,
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

async function handleSubmit() {
  const isValid = await formRef.value?.validate().catch(() => false)

  if (!isValid) {
    return
  }

  try {
    await postStore.createPost(form.title, form.content, form.allowComments)
    ElMessage.success('帖子创建成功')
    await router.push('/')
  } catch {
    ElMessage.error('帖子创建失败')
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
          <el-button size="large">保存草稿</el-button>
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
  justify-content: flex-end;
  gap: var(--space-12);
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
}
</style>
