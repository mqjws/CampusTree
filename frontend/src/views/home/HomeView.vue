<script setup lang="ts">
import { Bell, TrendCharts } from '@element-plus/icons-vue'
import { onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import AppLayout from '@/components/layout/AppLayout.vue'
import PostCard from '@/components/post/PostCard.vue'
import * as topicApi from '@/api/topic'
import { createPostCategories, mockNotices } from '@/mock/community'
import { usePostStore } from '@/stores/modules/post'
import { useUserStore } from '@/stores/modules/user'
import type { PostSort } from '@/api/post'
import type { TopicDto } from '@/types/api'

const router = useRouter()
const postStore = usePostStore()
const userStore = useUserStore()
const sortMode = ref<PostSort>('latest')
const activeCategory = ref('')
const activeTopicId = ref<number | null>(null)
const hotTopics = ref<TopicDto[]>([])
const loadingTopics = ref(false)
const sortOptions = [
  { label: '最新', value: 'latest' },
  { label: '热门', value: 'hot' },
]
const categoryOptions = [
  { label: '全部分类', value: '' },
  ...createPostCategories.map((category) => ({
    label: category,
    value: category,
  })),
]

function openPost(id: number) {
  router.push(`/post/${id}`)
}

onMounted(() => {
  fetchPostList()
  fetchHotTopics()
  userStore.fetchCurrentUser().catch(() => undefined)
})

watch([sortMode, activeCategory, activeTopicId], () => {
  fetchPostList()
})

function fetchPostList() {
  postStore
    .fetchPosts(
      1,
      10,
      sortMode.value,
      activeCategory.value || undefined,
      activeTopicId.value || undefined,
    )
    .catch(() => undefined)
}

async function fetchHotTopics() {
  loadingTopics.value = true

  try {
    const data = await topicApi.listHotTopics(8)
    hotTopics.value = data.items
  } catch {
    hotTopics.value = []
  } finally {
    loadingTopics.value = false
  }
}

function toggleTopic(topicId: number) {
  activeTopicId.value = activeTopicId.value === topicId ? null : topicId
}
</script>

<template>
  <AppLayout
    title="校园匿名流"
    description="按分类和话题浏览校园内容，热门话题会根据真实帖子实时更新。"
    :user-card="{
      nickname: userStore.profile.nickname,
      userId: userStore.profile.userId,
      tagline: userStore.profile.tagline,
    }"
  >
    <section class="home-toolbar">
      <div class="home-toolbar__tabs">
        <el-segmented v-model="sortMode" :options="sortOptions" />
        <el-select v-model="activeCategory" class="home-toolbar__category" size="large">
          <el-option
            v-for="category in categoryOptions"
            :key="category.value"
            :label="category.label"
            :value="category.value"
          />
        </el-select>
      </div>
      <el-button type="primary" size="large" @click="router.push('/create')">
        发布一条新内容
      </el-button>
    </section>

    <section v-loading="postStore.loading" class="home-list">
      <el-empty
        v-if="!postStore.loading && postStore.postList.length === 0"
        description="还没有帖子数据"
      />
      <PostCard
        v-for="post in postStore.postList"
        v-else
        :key="post.id"
        :post="post"
        @select="openPost"
      />
    </section>

    <template #sidebar>
      <div class="home-sidebar">
        <section class="sidebar-card">
          <div class="sidebar-card__header">
            <h2>热门话题</h2>
            <el-icon><TrendCharts /></el-icon>
          </div>
          <div class="topic-list">
            <el-empty
              v-if="!loadingTopics && hotTopics.length === 0"
              description="暂无热门话题"
            />
            <button
              v-for="topic in hotTopics"
              v-else
              :key="topic.id"
              class="topic-list__item"
              :class="{ 'topic-list__item--active': activeTopicId === topic.id }"
              type="button"
              @click="toggleTopic(topic.id)"
            >
              <span># {{ topic.name }}</span>
              <small>{{ topic.post_count }} 条</small>
            </button>
          </div>
        </section>

        <section class="sidebar-card">
          <div class="sidebar-card__header">
            <h2>产品公告</h2>
            <el-icon><Bell /></el-icon>
          </div>
          <article v-for="notice in mockNotices" :key="notice.id" class="notice-item">
            <h3>{{ notice.title }}</h3>
            <p>{{ notice.content }}</p>
          </article>
        </section>
      </div>
    </template>
  </AppLayout>
</template>

<style scoped>
.home-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-16);
  padding: var(--space-16);
  border: 1px solid rgba(229, 231, 235, 0.72);
  border-radius: var(--radius-12);
  background: rgba(255, 255, 255, 0.92);
  box-shadow: var(--shadow-card);
}

.home-list,
.home-sidebar {
  display: grid;
  gap: var(--space-16);
}

.home-toolbar__tabs {
  display: flex;
  align-items: center;
  gap: var(--space-12);
}

.home-toolbar__category {
  width: 148px;
}

.sidebar-card {
  padding: var(--space-16);
  border: 1px solid rgba(229, 231, 235, 0.72);
  border-radius: var(--radius-12);
  background: rgba(255, 255, 255, 0.92);
  box-shadow: var(--shadow-card);
}

.sidebar-card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-12);
  margin-bottom: var(--space-16);
  color: var(--color-text-primary);
}

.sidebar-card__header h2 {
  font-size: 18px;
  font-weight: 600;
}

.topic-list {
  display: grid;
  gap: var(--space-8);
}

.topic-list__item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-12);
  padding: var(--space-12);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-8);
  color: var(--color-text-primary);
  background: linear-gradient(180deg, #ffffff 0%, #f8fcfa 100%);
  cursor: pointer;
  transition:
    border-color 200ms ease,
    color 200ms ease,
    background 200ms ease;
}

.topic-list__item:hover,
.topic-list__item--active {
  border-color: rgba(16, 185, 129, 0.32);
  color: var(--color-primary);
  background: linear-gradient(180deg, #f0fdf4 0%, #ffffff 100%);
}

.topic-list__item small {
  color: var(--color-text-secondary);
}

.notice-item + .notice-item {
  margin-top: var(--space-16);
  padding-top: var(--space-16);
  border-top: 1px solid var(--color-border);
}

.notice-item h3 {
  margin-bottom: var(--space-8);
  color: var(--color-text-primary);
  font-size: 16px;
  font-weight: 600;
}

.notice-item p {
  color: var(--color-text-secondary);
  font-size: 14px;
  line-height: 1.7;
}

@media (max-width: 767px) {
  .home-toolbar {
    flex-direction: column;
    align-items: stretch;
  }

  .home-toolbar__tabs {
    flex-direction: column;
    align-items: stretch;
  }

  .home-toolbar__category {
    width: 100%;
  }
}
</style>
