import type { Router } from 'vue-router'
import { useAuthStore } from '@/stores/modules/auth'

export function setupRouterGuards(router: Router) {
  router.beforeEach(async (to) => {
    const authStore = useAuthStore()

    if (!authStore.initialized) {
      authStore.restoreAuth()
    }

    const requiresAuth = Boolean(to.meta.requiresAuth)

    if (requiresAuth && !authStore.isAuthenticated) {
      return {
        path: '/login',
        query: { redirect: to.fullPath },
      }
    }

    if (authStore.isAuthenticated && (to.path === '/login' || to.path === '/register')) {
      return { path: '/' }
    }

    return true
  })

  router.afterEach((to) => {
    document.title = typeof to.meta.title === 'string' ? to.meta.title : 'CampusTree'
  })
}
