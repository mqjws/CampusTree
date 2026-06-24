import type { Router } from 'vue-router'
import { useAuthStore } from '@/stores/modules/auth'
import { useUserStore } from '@/stores/modules/user'

export function setupRouterGuards(router: Router) {
  router.beforeEach(async (to) => {
    const authStore = useAuthStore()
    const userStore = useUserStore()

    if (!authStore.initialized) {
      authStore.restoreAuth()
      if (authStore.isAuthenticated) {
        await authStore.fetchCurrentUser().catch(() => {
          authStore.clearAuth()
        })
      }
    }

    const requiresAuth = Boolean(to.meta.requiresAuth)
    const requiresAdmin = Boolean(to.meta.requiresAdmin)

    if (requiresAuth && !authStore.isAuthenticated) {
      return {
        path: '/login',
        query: { redirect: to.fullPath },
      }
    }

    if (requiresAdmin) {
      if (!userStore.currentUser && authStore.isAuthenticated) {
        await authStore.fetchCurrentUser().catch(() => {
          authStore.clearAuth()
        })
      }

      if (userStore.currentUser?.role !== 'admin') {
        return { path: '/home' }
      }
    }

    if (
      authStore.isAuthenticated &&
      (to.path === '/' || to.path === '/login' || to.path === '/register')
    ) {
      return { path: '/home' }
    }

    return true
  })

  router.afterEach((to) => {
    document.title = typeof to.meta.title === 'string' ? to.meta.title : 'CampusTree'
  })
}
