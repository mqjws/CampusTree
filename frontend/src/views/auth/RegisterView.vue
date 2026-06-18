<script setup lang="ts">
import type { FormInstance, FormRules } from 'element-plus'
import { computed, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import AuthLayout from '@/components/layout/AuthLayout.vue'
import { useAuthStore } from '@/stores/modules/auth'

interface RegisterForm {
  username: string
  email: string
  password: string
  confirmPassword: string
  agree: boolean
}

const router = useRouter()
const authStore = useAuthStore()
const formRef = ref<FormInstance>()
const submitting = ref(false)

const form = reactive<RegisterForm>({
  username: 'campus_new_user',
  email: 'demo@campustree.local',
  password: 'demo123456',
  confirmPassword: 'demo123456',
  agree: true,
})

const passwordMatches = computed(() => form.password === form.confirmPassword)

const rules: FormRules<RegisterForm> = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 4, max: 20, message: '用户名长度为 4 到 20 个字符', trigger: 'blur' },
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效邮箱地址', trigger: ['blur', 'change'] },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 8, message: '密码至少 8 位', trigger: 'blur' },
  ],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    {
      validator: (_rule, value: string, callback) => {
        if (value !== form.password) {
          callback(new Error('两次输入的密码不一致'))
          return
        }

        callback()
      },
      trigger: ['blur', 'change'],
    },
  ],
  agree: [
    {
      validator: (_rule, value: boolean, callback) => {
        if (!value) {
          callback(new Error('请先确认继续使用当前演示流程'))
          return
        }

        callback()
      },
      trigger: 'change',
    },
  ],
}

const highlights = [
  {
    title: '最少阻力',
    description: '注册页先验证表单和交互节奏，再在下一阶段接入真实账户创建逻辑。',
  },
  {
    title: '设计一致',
    description: '表单、按钮、间距和文案层级都沿用 CampusTree 的设计系统令牌。',
  },
  {
    title: '安全占位',
    description: '当前不会提交任何真实数据，仅用于演示页面行为和路由跳转。',
  },
]

async function handleSubmit() {
  const isValid = await formRef.value?.validate().catch(() => false)

  if (!isValid || !passwordMatches.value) {
    return
  }

  submitting.value = true

  window.setTimeout(async () => {
    authStore.setToken('mock-campus-tree-token')
    await router.push('/')
    submitting.value = false
  }, 500)
}
</script>

<template>
  <AuthLayout
    caption="Register"
    title="创建你的匿名入口"
    description="先完成一版完整的注册页结构、表单校验和响应式布局，后续再接入真实注册 API。"
    :highlights="highlights"
  >
    <section class="auth-card">
      <div class="auth-card__header">
        <h2>注册</h2>
        <p>当前表单仅用于占位演示，提交后会模拟进入系统。</p>
      </div>

      <el-form ref="formRef" :model="form" :rules="rules" label-position="top" @submit.prevent>
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" size="large" />
        </el-form-item>

        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱地址" size="large" />
        </el-form-item>

        <div class="auth-card__row">
          <el-form-item class="auth-card__field" label="密码" prop="password">
            <el-input
              v-model="form.password"
              type="password"
              show-password
              placeholder="请输入密码"
              size="large"
            />
          </el-form-item>

          <el-form-item class="auth-card__field" label="确认密码" prop="confirmPassword">
            <el-input
              v-model="form.confirmPassword"
              type="password"
              show-password
              placeholder="请再次输入密码"
              size="large"
            />
          </el-form-item>
        </div>

        <el-form-item prop="agree">
          <el-checkbox v-model="form.agree" label="我已知晓当前为演示注册流程，不会创建真实账户" />
        </el-form-item>

        <div class="auth-card__footer">
          <RouterLink class="auth-card__link" to="/login">已有账号？去登录</RouterLink>
          <el-button
            class="auth-card__submit"
            type="primary"
            size="large"
            :loading="submitting"
            @click="handleSubmit"
          >
            创建账号
          </el-button>
        </div>
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

.auth-card__row {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--space-16);
}

.auth-card__field {
  margin-bottom: 0;
}

.auth-card__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-16);
  margin-top: var(--space-8);
}

.auth-card__link {
  color: var(--color-primary);
  font-size: 14px;
  font-weight: 500;
}

.auth-card__submit {
  min-width: 160px;
}

@media (max-width: 767px) {
  .auth-card {
    padding: var(--space-16);
  }

  .auth-card__row {
    grid-template-columns: minmax(0, 1fr);
    gap: 0;
  }

  .auth-card__footer {
    flex-direction: column;
    align-items: stretch;
  }

  .auth-card__submit {
    width: 100%;
  }
}
</style>
