import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import * as userApi from '@/api/user'
import { mapCommentDtoToRecord, mapPostDtoToRecord, mapUserToProfile } from '@/utils/mappers'
import type { CommentRecord, PostRecord, ProfileRecord, ProfileStats } from '@/types/content'
import type { UserDto } from '@/types/api'

export const useUserStore = defineStore('user', () => {
  const currentUser = ref<UserDto | null>(null)
  const myPosts = ref<PostRecord[]>([])
  const myComments = ref<CommentRecord[]>([])
  const stats = ref<ProfileStats>({
    posts: 0,
    comments: 0,
    likes: 0,
    views: 0,
    latestPostAt: null,
    latestCommentAt: null,
  })
  const loading = ref(false)
  const error = ref<string | null>(null)

  const profile = computed<ProfileRecord>(() => mapUserToProfile(currentUser.value, stats.value))

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

  async function fetchMyPosts() {
    loading.value = true
    error.value = null

    try {
      const data = await userApi.getMyPosts()
      myPosts.value = data.items.map(mapPostDtoToRecord)
    } catch (err) {
      error.value = '获取我的帖子失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchMyComments() {
    loading.value = true
    error.value = null

    try {
      const data = await userApi.getMyComments()
      myComments.value = data.items.map(mapCommentDtoToRecord)
    } catch (err) {
      error.value = '获取我的评论失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchMyStats() {
    loading.value = true
    error.value = null

    try {
      const data = await userApi.getMyStats()
      stats.value = {
        posts: data.post_count,
        comments: data.comment_count,
        likes: data.like_count,
        views: data.view_count,
        latestPostAt: data.latest_post_at,
        latestCommentAt: data.latest_comment_at,
      }
    } catch (err) {
      error.value = '获取用户统计失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateMyProfile(nickname: string) {
    loading.value = true
    error.value = null

    try {
      currentUser.value = await userApi.updateMyProfile({ nickname })
    } catch (err) {
      error.value = '更新个人资料失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  function clearUser() {
    currentUser.value = null
    myPosts.value = []
    myComments.value = []
    stats.value = {
      posts: 0,
      comments: 0,
      likes: 0,
      views: 0,
      latestPostAt: null,
      latestCommentAt: null,
    }
  }

  return {
    currentUser,
    myPosts,
    myComments,
    stats,
    loading,
    error,
    profile,
    fetchCurrentUser,
    fetchMyPosts,
    fetchMyComments,
    fetchMyStats,
    updateMyProfile,
    clearUser,
  }
})
