<script setup lang="ts">
import type { FormInstance, FormRules } from 'element-plus'
import { reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AuthLayout from '@/components/layout/AuthLayout.vue'
import { useAuthStore } from '@/stores/modules/auth'

interface LoginForm {
  account: string
  password: string
  rememberMe: boolean
}

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const formRef = ref<FormInstance>()
const submitting = ref(false)

const form = reactive<LoginForm>({
  account: 'campustree_demo',
  password: 'demo123456',
  rememberMe: true,
})

const rules: FormRules<LoginForm> = {
  account: [
    { required: true, message: '请输入用户名或邮箱', trigger: 'blur' },
    { min: 4, message: '至少输入 4 个字符', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 8, message: '密码至少 8 位', trigger: 'blur' },
  ],
}

const highlights = [
  {
    title: '低压表达',
    description: '减少熟人社交负担，让内容本身先被看见。',
  },
  {
    title: '移动优先',
    description: '认证流程保持轻量，适合在课堂间隙或通勤中快速进入。',
  },
  {
    title: '后续接 API',
    description: '当前提交仅使用占位数据，后续会替换成真实登录接口。',
  },
]

async function handleSubmit() {
  const isValid = await formRef.value?.validate().catch(() => false)

  if (!isValid) {
    return
  }

  submitting.value = true

  window.setTimeout(async () => {
    authStore.setToken('mock-campus-tree-token')

    const redirect = typeof route.query.redirect === 'string' ? route.query.redirect : '/'
    await router.push(redirect)
    submitting.value = false
  }, 500)
}
</script>

<template>
  <AuthLayout
    caption="Login"
    title="回到 CampusTree"
    description="登录后即可进入匿名校园社区。当前页面使用占位数据模拟提交流程，后续再接入真实认证接口。"
    :highlights="highlights"
  >
    <section class="auth-card">
      <div class="auth-card__header">
        <h2>登录</h2>
        <p>使用演示账号体验页面流程，当前不会请求后端。</p>
      </div>

      <el-form ref="formRef" :model="form" :rules="rules" label-position="top" @submit.prevent>
        <el-form-item label="用户名或邮箱" prop="account">
          <el-input v-model="form.account" placeholder="请输入用户名或邮箱" size="large" />
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input
            v-model="form.password"
            type="password"
            show-password
            placeholder="请输入密码"
            size="large"
          />
        </el-form-item>

        <div class="auth-card__options">
          <el-checkbox v-model="form.rememberMe" label="记住我" />
          <RouterLink class="auth-card__link" to="/register">还没有账号？去注册</RouterLink>
        </div>

        <el-button
          class="auth-card__submit"
          type="primary"
          size="large"
          :loading="submitting"
          @click="handleSubmit"
        >
          登录 CampusTree
        </el-button>
      </el-form>

      <div class="auth-card__hint">
        <span>演示账号：`campustree_demo`</span>
        <span>演示密码：`demo123456`</span>
      </div>
    </section>
  </AuthLayout>
</template>

<style scoped>
.auth-card {
  padding: var(--space-24);
  border: 1px solid rgba(229, 231, 235, 0.76);
  border-radius: var(--radius-16);
  background: rgba(255, 255, 255, 0.94);
  box-shadow: var(--shadow-modal);
}

.auth-card__header {
  margin-bottom: var(--space-24);
}

.auth-card__header h2 {
  margin-bottom: var(--space-8);
  color: var(--color-text-primary);
  font-size: 24px;
  line-height: 1.33;
}

.auth-card__header p {
  color: var(--color-text-secondary);
  font-size: 14px;
  line-height: 1.7;
}

.auth-card :deep(.el-form-item__label) {
  color: var(--color-text-primary);
  font-weight: 500;
}

.auth-card__options {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-12);
  margin-bottom: var(--space-24);
}

.auth-card__link {
  color: var(--color-primary);
  font-size: 14px;
  font-weight: 500;
}

.auth-card__submit {
  width: 100%;
}

.auth-card__hint {
  display: grid;
  gap: var(--space-8);
  margin-top: var(--space-16);
  color: var(--color-text-secondary);
  font-size: 13px;
}

@media (max-width: 767px) {
  .auth-card {
    padding: var(--space-16);
  }

  .auth-card__options {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
