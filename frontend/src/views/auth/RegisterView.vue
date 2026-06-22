<script setup lang="ts">
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'
import { computed, onBeforeUnmount, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { sendEmailCode } from '@/api/auth'
import AuthLayout from '@/components/layout/AuthLayout.vue'
import { useAuthStore } from '@/stores/modules/auth'

interface RegisterForm {
  username: string
  email: string
  emailCode: string
  password: string
  confirmPassword: string
  agree: boolean
}

const router = useRouter()
const authStore = useAuthStore()
const formRef = ref<FormInstance>()
const sendingEmailCode = ref(false)
const emailCodeCountdown = ref(0)
let countdownTimer: number | undefined

const form = reactive<RegisterForm>({
  username: '',
  email: '',
  emailCode: '',
  password: '',
  confirmPassword: '',
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
  emailCode: [
    { required: true, message: '请输入邮箱验证码', trigger: 'blur' },
    { len: 6, message: '验证码为 6 位数字', trigger: 'blur' },
    { pattern: /^\d{6}$/, message: '验证码为 6 位数字', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 5, message: '密码至少 5 位', trigger: 'blur' },
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
          callback(new Error('请确认后再继续'))
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
    title: '真实注册',
    description: '当前注册表单已接入真实后端接口。',
  },
  {
    title: '设计一致',
    description: '页面仍沿用 CampusTree 认证布局和设计系统。',
  },
  {
    title: '下一步登录',
    description: '注册成功后会跳转到登录页，使用刚创建的账号继续联调。',
  },
]

const canSendEmailCode = computed(() => {
  return Boolean(form.email) && emailCodeCountdown.value === 0 && !sendingEmailCode.value
})

function startEmailCodeCountdown() {
  emailCodeCountdown.value = 60
  countdownTimer = window.setInterval(() => {
    emailCodeCountdown.value -= 1

    if (emailCodeCountdown.value <= 0 && countdownTimer) {
      window.clearInterval(countdownTimer)
      countdownTimer = undefined
    }
  }, 1000)
}

async function handleSendEmailCode() {
  const isEmailValid = await formRef.value?.validateField('email').catch(() => false)

  if (isEmailValid === false || !canSendEmailCode.value) {
    return
  }

  sendingEmailCode.value = true

  try {
    const result = await sendEmailCode({ email: form.email })
    if (result.code) {
      form.emailCode = result.code
      ElMessage.success(`验证码已发送（开发模式，已自动填入：${result.code}）`)
    } else {
      ElMessage.success('验证码已发送，请查收邮箱')
    }
    startEmailCodeCountdown()
  } catch {
    ElMessage.error('验证码发送失败，请稍后重试')
  } finally {
    sendingEmailCode.value = false
  }
}

async function handleSubmit() {
  const isValid = await formRef.value?.validate().catch(() => false)

  if (!isValid || !passwordMatches.value) {
    return
  }

  try {
    await authStore.register({
      username: form.username,
      email: form.email,
      password: form.password,
      email_code: form.emailCode,
    })

    ElMessage.success('注册成功，请登录')
    await router.push('/login')
  } catch {
    ElMessage.error('注册失败，请检查用户名或邮箱是否已存在')
  }
}

onBeforeUnmount(() => {
  if (countdownTimer) {
    window.clearInterval(countdownTimer)
  }
})
</script>

<template>
  <AuthLayout
    caption="Register"
    title="创建你的匿名入口"
    description="先完成账号创建，再回到登录页进入 CampusTree。当前页面已接入真实注册接口。"
    :highlights="highlights"
  >
    <section class="auth-card">
      <div class="auth-card__header">
        <h2>注册</h2>
        <p>提交后会调用后端注册接口。</p>
      </div>

      <el-form ref="formRef" :model="form" :rules="rules" label-position="top" @submit.prevent>
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="form.username"
            autocomplete="username"
            placeholder="请输入用户名"
            size="large"
          />
        </el-form-item>

        <el-form-item label="邮箱" prop="email">
          <div class="auth-card__email-row">
            <el-input
              v-model="form.email"
              autocomplete="email"
              placeholder="请输入邮箱地址"
              size="large"
            />
            <el-button
              size="large"
              :loading="sendingEmailCode"
              :disabled="!canSendEmailCode"
              @click="handleSendEmailCode"
            >
              {{ emailCodeCountdown > 0 ? `${emailCodeCountdown}s` : '获取验证码' }}
            </el-button>
          </div>
        </el-form-item>

        <el-form-item label="邮箱验证码" prop="emailCode">
          <el-input
            v-model="form.emailCode"
            autocomplete="one-time-code"
            inputmode="numeric"
            maxlength="6"
            name="campustree_email_code"
            placeholder="请输入 6 位验证码"
            size="large"
          />
        </el-form-item>

        <div class="auth-card__row">
          <el-form-item class="auth-card__field" label="密码" prop="password">
            <el-input
              v-model="form.password"
              autocomplete="new-password"
              type="password"
              show-password
              name="campustree_register_password"
              placeholder="请输入密码"
              size="large"
            />
          </el-form-item>

          <el-form-item class="auth-card__field" label="确认密码" prop="confirmPassword">
            <el-input
              v-model="form.confirmPassword"
              autocomplete="new-password"
              type="password"
              show-password
              name="campustree_register_confirm_password"
              placeholder="请再次输入密码"
              size="large"
            />
          </el-form-item>
        </div>

        <el-form-item prop="agree">
          <el-checkbox v-model="form.agree" label="我已确认使用当前信息创建账户" />
        </el-form-item>

        <div class="auth-card__footer">
          <RouterLink class="auth-card__link" to="/login">已有账号？去登录</RouterLink>
          <el-button
            class="auth-card__submit"
            type="primary"
            size="large"
            :loading="authStore.loading"
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

.auth-card__email-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 128px;
  gap: var(--space-12);
  width: 100%;
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

  .auth-card__email-row {
    grid-template-columns: minmax(0, 1fr);
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
