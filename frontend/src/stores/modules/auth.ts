import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

const TOKEN_KEY = 'campus_tree_token'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(null)
  const initialized = ref(false)

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
  }

  return {
    token,
    initialized,
    isAuthenticated,
    restoreAuth,
    setToken,
    clearAuth,
  }
})
