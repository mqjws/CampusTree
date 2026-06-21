<script setup lang="ts">
import { Bell, Close, Search, TrendCharts } from '@element-plus/icons-vue'
import { computed, onMounted, ref, watch } from 'vue'
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
const searchKeyword = ref('')
const hotTopics = ref<TopicDto[]>([])
const searchHistory = ref<string[]>([])
const loadingTopics = ref(false)
const searchHistoryKey = 'campus_tree_search_history'
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

const activeKeyword = computed(() => searchKeyword.value.trim())
const hasActiveFilters = computed(
  () =>
    Boolean(activeKeyword.value) ||
    Boolean(activeCategory.value) ||
    activeTopicId.value !== null,
)

function openPost(id: number) {
  router.push(`/post/${id}`)
}

onMounted(() => {
  loadSearchHistory()
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
      activeKeyword.value || undefined,
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

function querySearchSuggestions(query: string, callback: (items: { value: string }[]) => void) {
  const normalizedQuery = query.trim().toLowerCase()
  const historyItems = searchHistory.value
  const topicItems = hotTopics.value.map((topic) => topic.name)
  const categoryItems = createPostCategories
  const suggestions = [...new Set([...historyItems, ...topicItems, ...categoryItems])]
    .filter((item) => !normalizedQuery || item.toLowerCase().includes(normalizedQuery))
    .slice(0, 8)
    .map((value) => ({ value }))

  callback(suggestions)
}

function handleSearch() {
  const keyword = activeKeyword.value
  if (keyword) {
    saveSearchKeyword(keyword)
  }

  fetchPostList()
}

function clearSearch() {
  searchKeyword.value = ''
  fetchPostList()
}

function clearAllFilters() {
  searchKeyword.value = ''
  activeCategory.value = ''
  activeTopicId.value = null
  fetchPostList()
}

function loadSearchHistory() {
  try {
    const raw = localStorage.getItem(searchHistoryKey)
    const parsed = raw ? JSON.parse(raw) : []
    searchHistory.value = Array.isArray(parsed)
      ? parsed.filter((item): item is string => typeof item === 'string').slice(0, 8)
      : []
  } catch {
    searchHistory.value = []
  }
}

function saveSearchKeyword(keyword: string) {
  searchHistory.value = [keyword, ...searchHistory.value.filter((item) => item !== keyword)].slice(0, 8)
  localStorage.setItem(searchHistoryKey, JSON.stringify(searchHistory.value))
}

function clearSearchHistory() {
  searchHistory.value = []
  localStorage.removeItem(searchHistoryKey)
}

function applyHistoryKeyword(keyword: string) {
  searchKeyword.value = keyword
  handleSearch()
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
      <div class="home-toolbar__search">
        <el-autocomplete
          v-model="searchKeyword"
          class="home-search"
          size="large"
          clearable
          :fetch-suggestions="querySearchSuggestions"
          placeholder="搜索标题或内容"
          @select="handleSearch"
          @keyup.enter="handleSearch"
          @clear="clearSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-autocomplete>
        <el-button type="primary" size="large" @click="handleSearch">搜索</el-button>
      </div>
      <el-button type="primary" size="large" @click="router.push('/create')">
        发布一条新内容
      </el-button>
    </section>

    <section v-if="hasActiveFilters || searchHistory.length > 0" class="home-search-panel">
      <div v-if="hasActiveFilters" class="home-search-panel__active">
        <span v-if="activeKeyword">关键词：{{ activeKeyword }}</span>
        <span v-if="activeCategory">分类：{{ activeCategory }}</span>
        <span v-if="activeTopicId">
          话题：{{ hotTopics.find((topic) => topic.id === activeTopicId)?.name || activeTopicId }}
        </span>
        <el-button :icon="Close" text @click="clearAllFilters">清空筛选</el-button>
      </div>
      <div v-if="searchHistory.length > 0" class="home-search-panel__history">
        <span>搜索历史</span>
        <button
          v-for="keyword in searchHistory"
          :key="keyword"
          class="history-chip"
          type="button"
          @click="applyHistoryKeyword(keyword)"
        >
          {{ keyword }}
        </button>
        <el-button text @click="clearSearchHistory">清除</el-button>
      </div>
    </section>

    <section v-loading="postStore.loading" class="home-list">
      <el-empty
        v-if="!postStore.loading && postStore.postList.length === 0"
        :description="activeKeyword ? '没有找到相关帖子' : '还没有帖子数据'"
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

.home-toolbar__search {
  display: flex;
  flex: 1;
  min-width: 260px;
  gap: var(--space-8);
}

.home-search {
  width: 100%;
}

.home-search-panel {
  display: grid;
  gap: var(--space-12);
  padding: var(--space-16);
  border: 1px solid rgba(229, 231, 235, 0.72);
  border-radius: var(--radius-12);
  background: rgba(255, 255, 255, 0.92);
  box-shadow: var(--shadow-card);
}

.home-search-panel__active,
.home-search-panel__history {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--space-8);
  color: var(--color-text-secondary);
  font-size: 14px;
}

.home-search-panel__active span {
  padding: 6px var(--space-12);
  border-radius: var(--radius-8);
  color: var(--color-primary);
  background: #ecfdf5;
}

.history-chip {
  padding: 6px var(--space-12);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-8);
  color: var(--color-text-primary);
  background: #ffffff;
  cursor: pointer;
  transition:
    border-color 200ms ease,
    color 200ms ease;
}

.history-chip:hover {
  border-color: rgba(16, 185, 129, 0.32);
  color: var(--color-primary);
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

  .home-toolbar__search {
    min-width: 0;
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
