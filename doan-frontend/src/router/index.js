import { createRouter, createWebHistory } from 'vue-router'
import LocalStorageWorker from "@/common/storageHelper"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Login.vue')
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/Dashboard.vue')
    }
  ]
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = LocalStorageWorker.getToken()
  if (to.name !== 'login' && !isAuthenticated) next({ name: 'login' })
  else next()
})

export default router
