<script setup lang="ts">
import type { FormInstance, FormRules } from 'element-plus'
import { reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import AppLayout from '@/components/layout/AppLayout.vue'
import { createPostCategories, mockProfile } from '@/mock/community'

interface CreatePostForm {
  title: string
  category: string
  content: string
  allowComments: boolean
}

const formRef = ref<FormInstance>()
const submitting = ref(false)

const form = reactive<CreatePostForm>({
  title: '今晚操场夜跑的人比想象中多',
  category: createPostCategories[0],
  content: '这里是占位内容，用于演示发布页的布局、表单和文案结构。',
  allowComments: true,
})

const rules: FormRules<CreatePostForm> = {
  title: [
    { required: true, message: '请输入标题', trigger: 'blur' },
    { min: 6, max: 60, message: '标题长度为 6 到 60 个字符', trigger: 'blur' },
  ],
  category: [{ required: true, message: '请选择分类', trigger: 'change' }],
  content: [
    { required: true, message: '请输入正文', trigger: 'blur' },
    { min: 20, message: '正文至少输入 20 个字符', trigger: 'blur' },
  ],
}

async function handleSubmit() {
  const isValid = await formRef.value?.validate().catch(() => false)

  if (!isValid) {
    return
  }

  submitting.value = true

  window.setTimeout(() => {
    submitting.value = false
    ElMessage.success('当前为占位提交流程，后续将接入真实发帖接口。')
  }, 500)
}
</script>

<template>
  <AppLayout
    title="发布一条新内容"
    description="当前页面完成发帖流程的结构、表单和辅助说明布局。后续只需要替换为真实接口提交与错误处理逻辑。"
    :user-card="{
      nickname: mockProfile.nickname,
      userId: mockProfile.userId,
      tagline: mockProfile.tagline,
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
            <p>这里只是视觉与表单结构占位，真实逻辑后续接入。</p>
          </div>
          <el-switch v-model="form.allowComments" />
        </div>

        <div class="create-card__actions">
          <el-button size="large">保存草稿</el-button>
          <el-button type="primary" size="large" :loading="submitting" @click="handleSubmit">
            发布内容
          </el-button>
        </div>
      </el-form>
    </section>

    <template #sidebar>
      <div class="create-sidebar">
        <section class="sidebar-card">
          <h2>发帖建议</h2>
          <ul>
            <li>标题尽量直接表达核心信息。</li>
            <li>正文保留足够上下文，便于后续评论展开。</li>
            <li>本阶段仍为占位流程，不会写入后端。</li>
          </ul>
        </section>
      </div>
    </template>
  </AppLayout>
</template>

<style scoped>
.create-card,
.sidebar-card {
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

.create-card__options h2,
.sidebar-card h2 {
  margin-bottom: var(--space-8);
  color: var(--color-text-primary);
  font-size: 18px;
  font-weight: 600;
}

.create-card__options p,
.sidebar-card li {
  color: var(--color-text-secondary);
  font-size: 14px;
  line-height: 1.7;
}

.create-card__actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-12);
}

.sidebar-card ul {
  display: grid;
  gap: var(--space-12);
  padding-left: 20px;
}

@media (max-width: 767px) {
  .create-card,
  .sidebar-card {
    padding: var(--space-16);
  }

  .create-card__options,
  .create-card__actions {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>
