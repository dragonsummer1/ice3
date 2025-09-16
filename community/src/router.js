import { createRouter, createWebHistory } from 'vue-router'
import HomeView from './views/HomeView.vue'
import TransportView from './views/TransportView.vue'
import TipsView from './views/TipsView.vue'
import ForumView from './views/ForumView.vue'
import LoginView from './views/LoginView.vue'
import RegisterView from './views/RegisterView.vue'
import AdminDashboard from './views/AdminDashboard.vue'
import AdminDashboardHome from './views/AdminDashboardHome.vue'
import AdminUsersView from './views/AdminUsersView.vue'
import AdminTopicsView from './views/AdminTopicsView.vue'
import AdminCommentsView from './views/AdminCommentsView.vue'
import { useAuthStore } from './stores/auth.js'

// 导航守卫：检查用户是否登录
const requireAuth = (to, from, next) => {
  const authStore = useAuthStore()
  
  // 避免在登录页进行不必要的重定向
  if (to.path === '/login') {
    next()
    return
  }
  
  // 检查用户是否已登录
  if (!authStore.isAuthenticated) {
    next('/login')
  } else {
    next()
  }
}

// 导航守卫：检查用户是否是管理员
const requireAdmin = (to, from, next) => {
  const authStore = useAuthStore()
  
  // 避免在登录页进行不必要的重定向
  if (to.path === '/login') {
    next()
    return
  }
  
  // 检查用户是否已登录且是管理员
  if (!authStore.isAuthenticated || !authStore.isAdmin) {
    next('/login')
  } else {
    next()
  }
}

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/transport',
    name: 'transport',
    component: TransportView
  },
  {
    path: '/travel-tips',
    name: 'travel-tips',
    component: TipsView
  },
  {
    path: '/forum',
    name: 'forum',
    component: ForumView,
    beforeEnter: requireAuth // 论坛需要登录才能访问
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView
  },
  {
    path: '/admin',
    component: AdminDashboard,
    beforeEnter: requireAdmin,
    children: [
      {
        path: 'dashboard',
        name: 'admin-dashboard',
        component: AdminDashboardHome
      },
      {
        path: 'users',
        name: 'admin-users',
        component: AdminUsersView
      },
      {
          path: 'topics',
          name: 'admin-topics',
          component: AdminTopicsView
        },
        {
          path: 'comments',
          name: 'admin-comments',
          component: AdminCommentsView
        }
      ]
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router