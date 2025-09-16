import { defineStore } from 'pinia';
import axios from 'axios';
import router from '../router.js';

// 设置axios基础URL
axios.defaults.baseURL = 'http://localhost:5000';
// 全局设置withCredentials，确保所有请求都能携带凭证
axios.defaults.withCredentials = true;

// 为当前标签页生成唯一ID
const generateTabId = () => {
  return 'tab_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
};

// 获取当前标签页ID，如果不存在则生成新的
const getTabId = () => {
  let tabId = sessionStorage.getItem('tabId');
  if (!tabId) {
    tabId = generateTabId();
    sessionStorage.setItem('tabId', tabId);
  }
  return tabId;
};

// 添加请求拦截器，确保跨域请求携带凭证和标签页ID
axios.interceptors.request.use(
  (config) => {
    config.withCredentials = true;
    // 在请求头中添加标签页ID
    config.headers['X-Tab-Id'] = getTabId();
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 导出store实例
export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isAuthenticated: false,
    loading: false,
    error: null,
    lastCheckTime: 0,
    CHECK_INTERVAL: 10000, // 10秒
    checkCount: 0 // 用于追踪调用次数
  }),
  
  getters: {
    isAdmin: (state) => state.user && state.user.is_admin,
  },
  
  actions: {
    // 用户注册
    async register(credentials) {
      this.loading = true;
      this.error = null;
      
      try {
        console.log('Attempting registration with:', credentials.username, credentials.email);
        console.log('Base URL:', axios.defaults.baseURL);
        console.log('Full URL:', axios.defaults.baseURL + '/api/auth/register');
        console.log('With credentials:', axios.defaults.withCredentials);
        
        // 正确的API URL - 后端蓝图配置为'/api/auth'
        const response = await axios.post('/api/auth/register', credentials);
        console.log('Registration response:', response.data);
        return response.data;
      } catch (error) {
        console.error('Registration error details:', {
          status: error.response?.status,
          data: error.response?.data,
          message: error.message,
          config: error.config,
          isAxiosError: error.isAxiosError,
          code: error.code
        });
        // 后端返回的错误字段是'error'
        this.error = error.response?.data?.error || '注册失败';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    // 用户登录
    async login(credentials) {
      this.loading = true;
      this.error = null;
      
      try {
        console.log('Attempting login with:', credentials.username);
        // 为当前登录生成新的标签页ID，确保与其他标签页隔离
        const newTabId = generateTabId();
        sessionStorage.setItem('tabId', newTabId);
        
        // 添加remember参数，确保会话持久性
        const loginData = {
          ...credentials,
          remember: false, // 不使用长期cookie，以支持标签页隔离
          tabId: newTabId // 传递标签页ID给后端
        };
        const response = await axios.post('/api/auth/login', loginData);
        const { user } = response.data;
        
        console.log('Login successful for user:', user.username, 'on tab:', newTabId);
        // 只保存用户信息到sessionStorage，避免不同标签页共享认证状态
        sessionStorage.setItem('user', JSON.stringify(user));
        this.user = user;
        this.isAuthenticated = true;
        // 登录成功后立即更新最后检查时间，避免短时间内重复检查
        this.lastCheckTime = Date.now();
        return response.data;
      } catch (error) {
        console.error('Login error details:', {
          status: error.response?.status,
          data: error.response?.data,
          message: error.message
        });
        this.error = error.response?.data?.error || '登录失败';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    // 用户登出
    async logout() {
      try {
        // 获取标签页ID
        const tabId = sessionStorage.getItem('tabId');
        // 发送注销请求到后端，携带标签页ID
        await axios.post('/api/auth/logout', { tabId });
      } catch (error) {
        console.error('Logout error:', error);
      } finally {
        // 清除sessionStorage中的用户信息
        sessionStorage.removeItem('user');
        sessionStorage.removeItem('tabId');
        // 清除store中的用户信息
        this.user = null;
        this.isAuthenticated = false;
        // 重定向到登录页面，使用router.push代替window.location.href以避免整页刷新
        if (!router.currentRoute.value.path.includes('/login')) {
          router.push('/login');
        }
      }
    },
    
    // 检查用户是否已登录
    async checkAuth() {
      const now = Date.now();
      // 如果距离上次调用不足20秒，则跳过（增加间隔以减少请求频率）
      if (now - this.lastCheckTime < 20000) {
        console.log('Skipping checkAuth - too frequent, last called:', new Date(this.lastCheckTime));
        return;
      }
      
      this.lastCheckTime = now;
      console.log('checkAuth called at:', new Date());
      
      // 只从sessionStorage获取用户信息，确保不同标签页可以有独立的认证状态
      const userData = sessionStorage.getItem('user');
      
      // 如果有用户信息，先加载到store中
      if (userData) {
        try {
          this.user = JSON.parse(userData);
          this.isAuthenticated = true;
          console.log('User authenticated from storage');
          
          // 同时尝试通过API验证，如果验证失败也不清除本地用户信息
          try {
            const response = await axios.get('/api/auth/check');
            if (response.data.authenticated) {
              // 如果API验证成功，更新用户信息
              const profileResponse = await axios.get('/api/auth/current-user');
              this.user = profileResponse.data.user;
              // 只更新sessionStorage中的用户信息
              sessionStorage.setItem('user', JSON.stringify(profileResponse.data.user));
            }
          } catch (apiError) {
            console.error('API验证失败，但保留本地用户信息:', apiError);
            // 不执行logout，继续使用本地用户信息
          }
          
          return;
        } catch (e) {
          console.log('Failed to parse user data from storage:', e);
        }
      }
      
      console.log('Making API call to /api/auth/check');
      
      try {
        const response = await axios.get('/api/auth/check');
        if (response.data.authenticated) {
          this.isAuthenticated = true;
          // 更新用户信息
          const profileResponse = await axios.get('/api/auth/current-user');
          this.user = profileResponse.data.user;
          // 只更新sessionStorage中的用户信息
          sessionStorage.setItem('user', JSON.stringify(profileResponse.data.user));
        } else {
          // API验证失败，检查是否有本地用户信息
          if (!this.user) {
            this.logout();
          }
        }
      } catch (error) {
        // 如果验证失败，检查是否有本地用户信息
        console.error('认证检查失败:', error);
        if (!this.user) {
          this.logout();
        }
      }
    },
    
    // 用于App.vue中检查用户登录状态的方法
    async checkAuthStatus() {
      // 直接调用checkAuth，让checkAuth内部处理频率限制
      // 避免重复检查导致的逻辑复杂
      await this.checkAuth();
    },
    
    // 清除错误信息
    clearError() {
      this.error = null;
    }
  }
});

// 添加默认导出，以便在router.js中可以使用默认导入
export default useAuthStore;