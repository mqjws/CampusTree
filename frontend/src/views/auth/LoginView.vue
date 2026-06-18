<script setup lang="ts">
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'
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

const form = reactive<LoginForm>({
  account: '',
  password: '',
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
    title: '真实联调',
    description: '当前表单已改为真实登录接口，请使用后端可用账号进行测试。',
  },
]

async function handleSubmit() {
  const isValid = await formRef.value?.validate().catch(() => false)

  if (!isValid) {
    return
  }

  try {
    await authStore.login({
      account: form.account,
      password: form.password,
    })

    ElMessage.success('登录成功')
    const redirect = typeof route.query.redirect === 'string' ? route.query.redirect : '/'
    await router.push(redirect)
  } catch {
    ElMessage.error('登录失败，请检查账号或密码')
  }
}
</script>

<template>
  <AuthLayout
    caption="Login"
    title="回到 CampusTree"
    description="登录后即可进入匿名校园社区。当前页面已接入真实登录接口，但整体 UI 风格保持不变。"
    :highlights="highlights"
  >
    <section class="auth-card">
      <div class="auth-card__header">
        <h2>登录</h2>
        <p>输入后端已存在的账号信息完成联调。</p>
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
          :loading="authStore.loading"
          @click="handleSubmit"
        >
          登录 CampusTree
        </el-button>
      </el-form>
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
