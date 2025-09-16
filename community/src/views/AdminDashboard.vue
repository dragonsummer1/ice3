<template>
  <el-container class="admin-container">
    <el-header class="admin-header">
      <div class="header-left">
        <img src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" alt="Logo" class="logo">
        <span class="system-name">社区管理系统</span>
      </div>
      <div class="header-right">
        <el-dropdown>
          <span class="user-info">
            <el-avatar :size="32">{{ userInitial }}</el-avatar>
            <span>{{ currentUser?.username }}</span>
            <i class="el-icon-arrow-down el-icon--right"></i>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="handleLogout">
                <i class="el-icon-logout"></i>
                <span>退出登录</span>
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </el-header>
    
    <el-container>
      <el-aside width="200px" class="admin-sidebar">
        <el-menu 
          :default-active="activeMenu"
          class="admin-menu"
          background-color="#545c64"
          text-color="#fff"
          active-text-color="#ffd04b"
          router
        >
          <el-menu-item index="/admin/dashboard">
            <i class="el-icon-s-data"></i>
            <span>仪表盘</span>
          </el-menu-item>
          <el-menu-item index="/admin/users">
            <i class="el-icon-user"></i>
            <span>用户管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/comments">
            <i class="el-icon-chat-line-round"></i>
            <span>评论管理</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      
      <el-main class="admin-main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import { useAuthStore } from '../stores/auth.js';
import { useRouter, useRoute } from 'vue-router';
import { onMounted, computed } from 'vue';

export default {
  name: 'AdminDashboard',
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();
    const route = useRoute();
    
    // 检查用户是否已登录且是管理员
    onMounted(() => {
      if (!authStore.isAuthenticated || !authStore.isAdmin) {
        router.push('/login');
      }
    });
    
    // 处理退出登录
    const handleLogout = () => {
      authStore.logout();
      router.push('/login');
    };
    
    // 计算当前活动菜单
    const activeMenu = computed(() => {
      return route.fullPath;
    });
    
    // 获取当前用户
    const currentUser = computed(() => {
      return authStore.user;
    });
    
    // 获取用户姓氏首字母
    const userInitial = computed(() => {
      return currentUser.value?.username?.charAt(0).toUpperCase() || 'U';
    });
    
    return {
      handleLogout,
      activeMenu,
      currentUser,
      userInitial
    };
  }
};
</script>

<style scoped>
.admin-container {
  height: 100vh;
}

.admin-header {
  background-color: #ffffff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.header-left {
  display: flex;
  align-items: center;
}

.logo {
  width: 40px;
  height: 40px;
  margin-right: 10px;
}

.system-name {
  font-size: 20px;
  font-weight: bold;
  color: #1890ff;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.user-info .el-avatar {
  margin-right: 10px;
}

.admin-sidebar {
  background-color: #545c64;
}

.admin-menu {
  height: 100%;
  border-right: none;
}

.admin-main {
  background-color: #f0f2f5;
  padding: 20px;
  overflow-y: auto;
}
</style>