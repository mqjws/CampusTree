import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import * as authApi from '@/api/auth'
import { useUserStore } from './user'
import type { LoginPayload, RegisterPayload } from '@/types/api'

const TOKEN_KEY = 'campus_tree_token'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(null)
  const initialized = ref(false)
  const loading = ref(false)

  const isAuthenticated = computed(() => Boolean(token.value))

  function restoreAuth() {
    token.value = localStorage.getItem(TOKEN_KEY)
    initialized.value = true
  }

  function setToken(value: string | null) {
    token.value = value

    if (value) {
      localStorage.setItem(TOKEN_KEY, value)
      return
    }

    localStorage.removeItem(TOKEN_KEY)
  }

  function clearAuth() {
    setToken(null)
    useUserStore().clearUser()
  }

  async function login(payload: LoginPayload) {
    loading.value = true

    try {
      const data = await authApi.login(payload)
      setToken(data.access_token)
      useUserStore().currentUser = data.user
      initialized.value = true
      return data.user
    } finally {
      loading.value = false
    }
  }

  async function register(payload: RegisterPayload) {
    loading.value = true

    try {
      return await authApi.register(payload)
    } finally {
      loading.value = false
    }
  }

  async function fetchCurrentUser() {
    if (!token.value) {
      return null
    }

    const userStore = useUserStore()
    const user = await authApi.getCurrentUser()
    userStore.currentUser = user
    return user
  }

  return {
    token,
    initialized,
    loading,
    isAuthenticated,
    restoreAuth,
    setToken,
    clearAuth,
    login,
    register,
    fetchCurrentUser,
  }
})
