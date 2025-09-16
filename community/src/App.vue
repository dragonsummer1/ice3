<template>
  <div id="app">
    <!-- 非管理员页面显示导航栏 -->
    <nav class="navbar" v-if="!isInAdminRoute">
      <div class="container">
        <h1 class="logo">哈尔滨冰雪旅游指南</h1>
        <ul class="nav-links">
          <li><router-link to="/">首页</router-link></li>
          <li><router-link to="/transport">交通票价</router-link></li>
          <li><router-link to="/travel-tips">旅游贴士</router-link></li>
          <li><router-link to="/forum">旅游论坛</router-link></li>
          
          <!-- 未登录状态显示登录/注册链接 -->
          <li v-if="!isAuthenticated"><router-link to="/login">登录</router-link></li>
          <li v-if="!isAuthenticated"><router-link to="/register">注册</router-link></li>
          
          <!-- 登录状态显示用户信息和后台管理链接 -->
          <li v-if="isAuthenticated" class="user-dropdown">
            <span class="user-name">{{ username }}</span>
            <ul class="dropdown-menu">
              <li v-if="isAdmin"><router-link to="/admin/dashboard">后台管理</router-link></li>
              <li><button @click="handleLogout" class="logout-btn">退出登录</button></li>
            </ul>
          </li>
        </ul>
      </div>
    </nav>
    <main class="main-content">
      <transition name="router-view" mode="out-in">
        <router-view :key="$route.fullPath" />
      </transition>
    </main>
    <!-- 非管理员页面显示页脚 -->
    <footer class="footer" v-if="!isInAdminRoute">
      <div class="container">
        <p>&copy; 2025 哈尔滨冰雪旅游指南. 保留所有权利.</p>
        <p>客服热线：400-639-1999</p>
    </div>
  </footer>
</div>
</template>

<script lang="ts"> 
import { useAuthStore } from './stores/auth.js'
import { useRouter, useRoute } from 'vue-router'
import { computed, onMounted, watch } from 'vue'

export default {
  name: 'App',
  components: {},

  
  
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    const route = useRoute()
    
    // 计算属性：用户登录状态
    const isAuthenticated = computed(() => authStore.isAuthenticated)
    
    // 计算属性：用户名
    const username = computed(() => authStore.user?.username || '')
    
    // 计算属性：是否是管理员
    const isAdmin = computed(() => authStore.isAdmin)
    
    // 计算属性：是否在管理员路由中
    const isInAdminRoute = computed(() => {
      return route.path.startsWith('/admin/')
    })
    
    // 处理退出登录
    const handleLogout = async () => {
      await authStore.logout()
    }
    
    // 在组件挂载时检查用户登录状态
    onMounted(() => {
      // 首次加载时只检查一次认证状态
      authStore.checkAuthStatus()
      // 添加页面载入动画
      document.querySelector('.main-content').classList.add('fade-in');
    })
    
    // 优化路由监听，只在特定条件下检查认证状态
    let lastCheckRoute = null
    watch(
      () => route.path,
      (newPath) => {
        // 只有当路由变化并且不是在频繁切换时才检查认证状态
        // 避免在登录页面和其他页面之间快速切换时的重复检查
        if (newPath !== lastCheckRoute && !newPath.includes('/login')) {
          lastCheckRoute = newPath
          // 使用带频率限制的checkAuthStatus方法
          authStore.checkAuthStatus()
        }
      }
    )
    
    return {
      isAuthenticated,
      username,
      isAdmin,
      handleLogout,
      isInAdminRoute
    }
  }
}
</script>

<style>
/* 导入全局动画样式 */
@import './assets/animations.css';

/* 页面过渡效果 */
.router-view-enter-active,
.router-view-leave-active {
  transition: all 0.5s ease;
}

.router-view-enter-from,
.router-view-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

.fade-in {
  animation: fadeIn 0.8s ease-in;
}
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  line-height: 1.6;
  color: #333;
  background-color: #f5f5f5;
}

.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.navbar {
  background: linear-gradient(135deg, #0056b3 0%, #003d82 100%);
  color: white;
  padding: 15px 0;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.navbar .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.8rem;
  font-weight: bold;
  text-shadow: 0 2px 4px rgba(0,0,0,0.2);
  transition: transform 0.3s ease;
}

.logo:hover {
  transform: scale(1.05);
}

.nav-links {
  display: flex;
  list-style: none;
  align-items: center;
}

.nav-links li {
  margin-left: 20px;
  position: relative;
}

/* 用户下拉菜单样式 */
.user-dropdown {
  position: relative;
}

.user-name {
  color: white;
  cursor: pointer;
  padding: 8px 15px;
  border-radius: 20px;
  transition: all 0.3s ease;
  position: relative;
}

.user-name:hover {
  background-color: rgba(255, 255, 255, 0.15);
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  padding: 10px 0;
  min-width: 150px;
  z-index: 1000;
  display: none;
}

.user-dropdown:hover .dropdown-menu {
  display: block;
}

.dropdown-menu li {
  margin: 0;
}

.dropdown-menu a,
.logout-btn {
  display: block;
  width: 100%;
  padding: 10px 20px;
  color: #333;
  text-decoration: none;
  background: none;
  border: none;
  text-align: left;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1rem;
}

.dropdown-menu a:hover,
.logout-btn:hover {
  background-color: #f8f9fa;
  color: #0056b3;
}

.nav-links a {
  color: white;
  text-decoration: none;
  font-size: 1.1rem;
  padding: 8px 15px;
  border-radius: 20px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.nav-links a::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 2px;
  background-color: white;
  transition: all 0.3s ease;
  transform: translateX(-50%);
}

.nav-links a:hover {
  background-color: rgba(255, 255, 255, 0.15);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.nav-links a:hover::after {
  width: 80%;
}

.main-content {
  min-height: calc(100vh - 140px);
  padding: 30px 0;
}

.footer {
  background-color: #333;
  color: white;
  padding: 20px 0;
  text-align: center;
}

.footer p {
  margin: 5px 0;
}
</style>