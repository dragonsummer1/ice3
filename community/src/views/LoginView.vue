<template>
  <div class="login-container">
    <div class="login-form">
      <h2>用户登录</h2>
      
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">用户名</label>
          <input
            type="text"
            id="username"
            v-model="credentials.username"
            required
            placeholder="请输入用户名"
            :disabled="loading"
          />
        </div>
        
        <div class="form-group">
          <label for="password">密码</label>
          <input
            type="password"
            id="password"
            v-model="credentials.password"
            required
            placeholder="请输入密码"
            :disabled="loading"
          />
        </div>
        
        <div v-if="error" :class="['error-message', {
          'username-error': error.includes('用户名'),
          'password-error': error.includes('密码')
        }]">
          <i v-if="error.includes('用户名')" class="error-icon">👤</i>
          <i v-else-if="error.includes('密码')" class="error-icon">🔒</i>
          <i v-else class="error-icon">⚠️</i>
          {{ error }}
        </div>
        
        <button type="submit" class="login-button" :disabled="loading">
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>
      
      <div class="register-link">
        还没有账号？<router-link to="/register">立即注册</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth.js';
import { useRouter } from 'vue-router';
import { onMounted } from 'vue';

export default {
  name: 'LoginView',
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();
    
    const credentials = {
      username: '',
      password: ''
    };
    
    // 在组件挂载时清除错误信息
    onMounted(() => {
      authStore.clearError();
    });
    
    // 处理登录逻辑
    const handleLogin = async () => {
      try {
        const result = await authStore.login(credentials);
        
        // 如果是管理员用户，提示是否进入管理界面
        if (result.user && result.user.is_admin) {
          if (confirm('您是管理员用户，是否进入管理界面？')) {
            router.push('/admin/dashboard');
          } else {
            router.push('/forum');
          }
        } else {
          // 普通用户继续跳转到论坛页面
          router.push('/forum');
        }
      } catch (error) {
        // 错误信息已经在authStore中处理
        console.error('Login failed:', error);
      }
    };
    
    return {
      credentials,
      handleLogin,
      loading: authStore.loading,
      error: authStore.error
    };
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 70vh;
  padding: 20px;
  background: linear-gradient(135deg, rgba(0, 86, 179, 0.03) 0%, rgba(0, 173, 239, 0.03) 100%);
}

.login-form {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.login-form h2 {
  text-align: center;
  color: #0056b3;
  margin-bottom: 30px;
  font-size: 1.8rem;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #0056b3;
  box-shadow: 0 0 0 3px rgba(0, 86, 179, 0.1);
}

.form-group input:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.error-message {
  color: #e74c3c;
  margin-bottom: 15px;
  padding: 10px;
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  border-radius: 6px;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.username-error {
  background-color: #fff3cd;
  border-color: #ffeaa7;
  color: #856404;
}

.password-error {
  background-color: #f8d7da;
  border-color: #f5c6cb;
  color: #721c24;
}

.error-icon {
  font-size: 1.2rem;
}

.login-button {
  width: 100%;
  padding: 12px;
  background: linear-gradient(45deg, #0056b3, #007bff);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.login-button:hover:not(:disabled) {
  background: linear-gradient(45deg, #004085, #0056b3);
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 86, 179, 0.3);
}

.login-button:active {
  transform: translateY(0);
}

.login-button:disabled {
  background: #6c757d;
  cursor: not-allowed;
  transform: none;
}

.register-link {
  text-align: center;
  margin-top: 20px;
  color: #666;
}

.register-link a {
  color: #0056b3;
  text-decoration: none;
  transition: color 0.3s ease;
}

.register-link a:hover {
  color: #004085;
  text-decoration: underline;
}
</style>