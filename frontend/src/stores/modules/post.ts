import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import * as postApi from '@/api/post'
import { mapPostDtoToRecord } from '@/utils/mappers'
import type { PostRecord } from '@/types/content'

export const usePostStore = defineStore('post', () => {
  const posts = ref<PostRecord[]>([])
  const currentPost = ref<PostRecord | null>(null)
  const loading = ref(false)
  const creating = ref(false)
  const error = ref<string | null>(null)

  const postList = computed(() => posts.value)

  async function fetchPosts(page = 1, size = 10) {
    loading.value = true
    error.value = null

    try {
      const data = await postApi.listPosts(page, size)
      posts.value = data.items.map(mapPostDtoToRecord)
    } catch (err) {
      error.value = '获取帖子列表失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchPostDetail(postId: number) {
    loading.value = true
    error.value = null

    try {
      const post = await postApi.getPostDetail(postId)
      currentPost.value = mapPostDtoToRecord(post)
    } catch (err) {
      error.value = '获取帖子详情失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createPost(title: string, content: string) {
    creating.value = true
    error.value = null

    try {
      const post = await postApi.createPost({ title, content })
      const mapped = mapPostDtoToRecord(post)
      posts.value.unshift(mapped)
      currentPost.value = mapped
      return mapped
    } catch (err) {
      error.value = '创建帖子失败'
      throw err
    } finally {
      creating.value = false
    }
  }

  async function like(postId: number) {
    await postApi.likePost(postId)
  }

  function incrementCommentCount(postId: number) {
    const update = (post: PostRecord) => {
      if (post.id === postId) {
        post.commentCount += 1
      }
    }

    posts.value.forEach(update)

    if (currentPost.value?.id === postId) {
      update(currentPost.value)
    }
  }

  async function unlike(postId: number) {
    await postApi.unlikePost(postId)
  }

  return {
    posts,
    currentPost,
    loading,
    creating,
    error,
    postList,
    fetchPosts,
    fetchPostDetail,
    createPost,
    incrementCommentCount,
    like,
    unlike,
  }
})
