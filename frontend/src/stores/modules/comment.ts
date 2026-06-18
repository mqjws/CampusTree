import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import * as commentApi from '@/api/comment'
import { mapCommentDtoToRecord } from '@/utils/mappers'
import type { CommentRecord } from '@/types/content'

export const useCommentStore = defineStore('comment', () => {
  const commentsByPostId = ref<Record<number, CommentRecord[]>>({})
  const loading = ref(false)
  const creating = ref(false)
  const error = ref<string | null>(null)

  const getComments = computed(() => (postId: number) => commentsByPostId.value[postId] || [])

  async function fetchComments(postId: number, page = 1, size = 20) {
    loading.value = true
    error.value = null

    try {
      const data = await commentApi.listCommentsByPost(postId, page, size)
      commentsByPostId.value[postId] = data.items.map(mapCommentDtoToRecord)
    } catch (err) {
      error.value = '获取评论列表失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createComment(postId: number, content: string) {
    creating.value = true
    error.value = null

    try {
      const comment = await commentApi.createComment(postId, { content })
      const mapped = mapCommentDtoToRecord(comment)
      commentsByPostId.value[postId] = [mapped, ...(commentsByPostId.value[postId] || [])]
      return mapped
    } catch (err) {
      error.value = '创建评论失败'
      throw err
    } finally {
      creating.value = false
    }
  }

  return {
    commentsByPostId,
    loading,
    creating,
    error,
    getComments,
    fetchComments,
    createComment,
  }
})
