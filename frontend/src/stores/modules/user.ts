import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import * as userApi from '@/api/user'
import { mapUserToProfile } from '@/utils/mappers'
import type { ProfileRecord } from '@/types/content'
import type { UserDto } from '@/types/api'

export const useUserStore = defineStore('user', () => {
  const currentUser = ref<UserDto | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const profile = computed<ProfileRecord>(() => mapUserToProfile(currentUser.value))

  async function fetchCurrentUser() {
    loading.value = true
    error.value = null

    try {
      currentUser.value = await userApi.getCurrentUser()
    } catch (err) {
      error.value = '获取当前用户失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  function clearUser() {
    currentUser.value = null
  }

  return {
    currentUser,
    loading,
    error,
    profile,
    fetchCurrentUser,
    clearUser,
  }
})
