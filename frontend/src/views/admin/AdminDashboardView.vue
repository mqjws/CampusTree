<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { Delete, Plus, Search } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import AppLayout from '@/components/layout/AppLayout.vue'
import * as adminApi from '@/api/admin'
import { useUserStore } from '@/stores/modules/user'
import type { PostDto, PostReportDto, SensitiveWordDto, UserDto } from '@/types/api'
import { formatFullTime } from '@/utils/format'

const userStore = useUserStore()
const activeTab = ref('users')

const users = ref<UserDto[]>([])
const posts = ref<PostDto[]>([])
const reports = ref<PostReportDto[]>([])
const words = ref<SensitiveWordDto[]>([])

const loadingUsers = ref(false)
const loadingPosts = ref(false)
const loadingReports = ref(false)
const loadingWords = ref(false)
const addingWord = ref(false)

const userKeyword = ref('')
const postKeyword = ref('')
const reportStatus = ref<'pending' | 'resolved' | 'ignored' | ''>('pending')
const wordKeyword = ref('')
const newWord = ref('')

const pendingReportCount = computed(() => {
  return reports.value.filter((report) => report.status === 'pending').length
})

onMounted(() => {
  userStore.fetchCurrentUser().catch(() => undefined)
  fetchUsers()
  fetchPosts()
  fetchReports()
  fetchWords()
})

async function fetchUsers() {
  loadingUsers.value = true
  try {
    const data = await adminApi.listUsers(userKeyword.value.trim() || undefined)
    users.value = data.items
  } catch {
    ElMessage.error('获取用户列表失败')
  } finally {
    loadingUsers.value = false
  }
}

async function handleToggleUser(user: UserDto) {
  const nextStatus = !user.is_active
  const action = nextStatus ? '解封' : '封禁'

  try {
    await ElMessageBox.confirm(`确认${action}用户「${user.username}」？`, `${action}确认`, {
      type: 'warning',
      confirmButtonText: action,
      cancelButtonText: '取消',
    })
    const updated = await adminApi.updateUserStatus(user.id, nextStatus)
    users.value = users.value.map((item) => (item.id === updated.id ? updated : item))
    ElMessage.success(`已${action}用户`)
  } catch {
    // 用户取消或请求失败
  }
}

async function handleDeleteUser(user: UserDto) {
  try {
    await ElMessageBox.confirm(
      `确认删除用户「${user.username}」？该操作会删除其内容。`,
      '删除确认',
      {
        type: 'warning',
        confirmButtonText: '删除',
        cancelButtonText: '取消',
      },
    )
    await adminApi.deleteUser(user.id)
    users.value = users.value.filter((item) => item.id !== user.id)
    ElMessage.success('用户已删除')
  } catch {
    // 用户取消或请求失败
  }
}

async function fetchPosts() {
  loadingPosts.value = true
  try {
    const data = await adminApi.listPosts(postKeyword.value.trim() || undefined)
    posts.value = data.items
  } catch {
    ElMessage.error('获取帖子列表失败')
  } finally {
    loadingPosts.value = false
  }
}

async function handleDeletePost(post: PostDto) {
  try {
    await ElMessageBox.confirm(`确认删除帖子「${post.title}」？`, '删除确认', {
      type: 'warning',
      confirmButtonText: '删除',
      cancelButtonText: '取消',
    })
    await adminApi.deleteAdminPost(post.id)
    posts.value = posts.value.filter((item) => item.id !== post.id)
    ElMessage.success('帖子已删除')
  } catch {
    // 用户取消或请求失败
  }
}

async function fetchReports() {
  loadingReports.value = true
  try {
    const data = await adminApi.listReports(reportStatus.value || undefined)
    reports.value = data.items
  } catch {
    ElMessage.error('获取举报列表失败')
  } finally {
    loadingReports.value = false
  }
}

async function handleUpdateReport(report: PostReportDto, status: 'resolved' | 'ignored') {
  try {
    const updated = await adminApi.updateReportStatus(report.id, status)
    reports.value = reports.value.map((item) => (item.id === updated.id ? updated : item))
    ElMessage.success(status === 'resolved' ? '举报已处理' : '举报已忽略')
  } catch {
    ElMessage.error('更新举报状态失败')
  }
}

async function fetchWords() {
  loadingWords.value = true
  try {
    const data = await adminApi.listSensitiveWords(wordKeyword.value.trim() || undefined)
    words.value = data.items
  } catch {
    ElMessage.error('获取敏感词列表失败')
  } finally {
    loadingWords.value = false
  }
}

async function handleAddWord() {
  const word = newWord.value.trim()
  if (!word) {
    ElMessage.warning('请输入敏感词')
    return
  }

  addingWord.value = true
  try {
    await adminApi.createSensitiveWord({ word })
    newWord.value = ''
    await fetchWords()
    ElMessage.success('敏感词已添加')
  } catch {
    ElMessage.error('添加失败，可能该敏感词已存在')
  } finally {
    addingWord.value = false
  }
}

async function handleDeleteWord(word: SensitiveWordDto) {
  try {
    await ElMessageBox.confirm(`确认删除敏感词「${word.word}」？`, '删除确认', {
      type: 'warning',
      confirmButtonText: '删除',
      cancelButtonText: '取消',
    })
    await adminApi.deleteSensitiveWord(word.id)
    words.value = words.value.filter((item) => item.id !== word.id)
    ElMessage.success('敏感词已删除')
  } catch {
    // 用户取消或请求失败
  }
}
</script>

<template>
  <AppLayout
    title="管理后台"
    description="查看用户、帖子、举报记录，并维护敏感词审核规则。"
    :user-card="{
      nickname: userStore.profile.nickname,
      userId: userStore.profile.userId,
      tagline: userStore.profile.tagline,
    }"
  >
    <section class="admin-dashboard">
      <el-tabs v-model="activeTab" class="admin-tabs">
        <el-tab-pane label="用户管理" name="users">
          <div class="admin-toolbar">
            <el-input
              v-model="userKeyword"
              :prefix-icon="Search"
              placeholder="搜索用户名、昵称或邮箱"
              clearable
              @keyup.enter="fetchUsers"
              @clear="fetchUsers"
            />
            <el-button type="primary" @click="fetchUsers">搜索</el-button>
          </div>

          <el-table v-loading="loadingUsers" :data="users" class="admin-table">
            <el-table-column prop="id" label="ID" width="72" />
            <el-table-column prop="username" label="用户名" min-width="120" />
            <el-table-column prop="nickname" label="昵称" min-width="120" />
            <el-table-column prop="email" label="邮箱" min-width="190" />
            <el-table-column label="角色" width="96">
              <template #default="{ row }">
                <el-tag :type="row.role === 'admin' ? 'danger' : 'info'" effect="plain">
                  {{ row.role }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="状态" width="96">
              <template #default="{ row }">
                <el-tag :type="row.is_active ? 'success' : 'warning'" effect="plain">
                  {{ row.is_active ? '正常' : '封禁' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="注册时间" min-width="170">
              <template #default="{ row }">{{ formatFullTime(row.created_at) }}</template>
            </el-table-column>
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="{ row }">
                <el-button
                  size="small"
                  :disabled="row.id === userStore.currentUser?.id"
                  @click="handleToggleUser(row)"
                >
                  {{ row.is_active ? '封禁' : '解封' }}
                </el-button>
                <el-button
                  type="danger"
                  size="small"
                  plain
                  :disabled="row.id === userStore.currentUser?.id"
                  @click="handleDeleteUser(row)"
                >
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="帖子管理" name="posts">
          <div class="admin-toolbar">
            <el-input
              v-model="postKeyword"
              :prefix-icon="Search"
              placeholder="搜索标题或正文"
              clearable
              @keyup.enter="fetchPosts"
              @clear="fetchPosts"
            />
            <el-button type="primary" @click="fetchPosts">搜索</el-button>
          </div>

          <el-table v-loading="loadingPosts" :data="posts" class="admin-table">
            <el-table-column prop="id" label="ID" width="72" />
            <el-table-column prop="title" label="标题" min-width="180" show-overflow-tooltip />
            <el-table-column prop="author_nickname" label="作者" min-width="120" />
            <el-table-column prop="category" label="分类" width="100" />
            <el-table-column label="可见性" width="130">
              <template #default="{ row }">
                <el-tag :type="row.registered_only ? 'warning' : 'success'" effect="plain">
                  {{ row.registered_only ? '注册用户' : '公开' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="comment_count" label="评论" width="84" />
            <el-table-column prop="like_count" label="点赞" width="84" />
            <el-table-column label="发布时间" min-width="170">
              <template #default="{ row }">{{ formatFullTime(row.created_at) }}</template>
            </el-table-column>
            <el-table-column label="操作" width="96" fixed="right">
              <template #default="{ row }">
                <el-button type="danger" size="small" plain @click="handleDeletePost(row)">
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane
          :label="`举报管理${pendingReportCount ? ` (${pendingReportCount})` : ''}`"
          name="reports"
        >
          <div class="admin-toolbar">
            <el-select
              v-model="reportStatus"
              placeholder="举报状态"
              clearable
              @change="fetchReports"
            >
              <el-option label="待处理" value="pending" />
              <el-option label="已处理" value="resolved" />
              <el-option label="已忽略" value="ignored" />
            </el-select>
            <el-button type="primary" @click="fetchReports">刷新</el-button>
          </div>

          <el-table v-loading="loadingReports" :data="reports" class="admin-table">
            <el-table-column prop="id" label="ID" width="72" />
            <el-table-column prop="post_title" label="帖子" min-width="170" show-overflow-tooltip />
            <el-table-column prop="reporter_username" label="举报人" min-width="120" />
            <el-table-column prop="reason" label="理由" width="110" />
            <el-table-column
              prop="description"
              label="说明"
              min-width="180"
              show-overflow-tooltip
            />
            <el-table-column label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="row.status === 'pending' ? 'warning' : 'info'" effect="plain">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="时间" min-width="170">
              <template #default="{ row }">{{ formatFullTime(row.created_at) }}</template>
            </el-table-column>
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="{ row }">
                <el-button
                  size="small"
                  type="primary"
                  plain
                  :disabled="row.status !== 'pending'"
                  @click="handleUpdateReport(row, 'resolved')"
                >
                  已处理
                </el-button>
                <el-button
                  size="small"
                  plain
                  :disabled="row.status !== 'pending'"
                  @click="handleUpdateReport(row, 'ignored')"
                >
                  忽略
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="敏感词管理" name="words">
          <div class="admin-toolbar admin-toolbar--stacked">
            <div class="admin-toolbar__row">
              <el-input
                v-model="wordKeyword"
                :prefix-icon="Search"
                placeholder="搜索敏感词"
                clearable
                @keyup.enter="fetchWords"
                @clear="fetchWords"
              />
              <el-button type="primary" @click="fetchWords">搜索</el-button>
            </div>
            <div class="admin-toolbar__row">
              <el-input
                v-model="newWord"
                placeholder="输入新敏感词"
                maxlength="50"
                show-word-limit
                @keyup.enter="handleAddWord"
              />
              <el-button type="primary" :loading="addingWord" :icon="Plus" @click="handleAddWord">
                添加
              </el-button>
            </div>
          </div>

          <el-table v-loading="loadingWords" :data="words" class="admin-table">
            <el-table-column prop="id" label="ID" width="72" />
            <el-table-column prop="word" label="敏感词" min-width="160" />
            <el-table-column label="创建时间" min-width="170">
              <template #default="{ row }">{{ formatFullTime(row.created_at) }}</template>
            </el-table-column>
            <el-table-column label="操作" width="96" fixed="right">
              <template #default="{ row }">
                <el-button
                  type="danger"
                  :icon="Delete"
                  size="small"
                  plain
                  @click="handleDeleteWord(row)"
                >
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </section>
  </AppLayout>
</template>

<style scoped>
.admin-dashboard {
  padding: var(--space-24);
  border: 1px solid rgba(229, 231, 235, 0.76);
  border-radius: var(--radius-16);
  background: rgba(255, 255, 255, 0.94);
  box-shadow: var(--shadow-card);
}

.admin-toolbar {
  display: flex;
  align-items: center;
  gap: var(--space-12);
  margin-bottom: var(--space-16);
}

.admin-toolbar .el-input {
  max-width: 360px;
}

.admin-toolbar--stacked {
  display: grid;
}

.admin-toolbar__row {
  display: flex;
  gap: var(--space-12);
}

.admin-table {
  width: 100%;
}

@media (max-width: 767px) {
  .admin-dashboard {
    padding: var(--space-16);
  }

  .admin-toolbar,
  .admin-toolbar__row {
    align-items: stretch;
    flex-direction: column;
  }

  .admin-toolbar .el-input {
    max-width: none;
  }
}
</style>
