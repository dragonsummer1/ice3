<template>
  <div class="register-container">
    <div class="register-form">
      <h2>用户注册</h2>
      
      <form @submit.prevent="handleRegister">
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
          <label for="email">邮箱</label>
          <input
            type="email"
            id="email"
            v-model="credentials.email"
            required
            placeholder="请输入邮箱"
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
            placeholder="请输入密码（至少6位）"
            :disabled="loading"
          />
        </div>
        
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        
        <button type="submit" class="register-button" :disabled="loading">
          {{ loading ? '注册中...' : '注册' }}
        </button>
      </form>
      
      <div class="login-link">
        已有账号？<router-link to="/login">立即登录</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth.js';
import { useRouter } from 'vue-router';
import { onMounted, reactive } from 'vue';

export default {
  name: 'RegisterView',
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();
    
    const credentials = reactive({
      username: '',
      email: '',
      password: ''
    });
    
    // 在组件挂载时清除错误信息
    onMounted(() => {
      authStore.clearError();
    });
    
    // 处理注册逻辑
    const handleRegister = async () => {
      try {
        await authStore.register(credentials);
        // 注册成功后跳转到登录页
        router.push('/login');
      } catch (error) {
        // 错误信息已经在authStore中处理
        console.error('Registration failed:', error);
      }
    };
    
    return {
      credentials,
      handleRegister,
      loading: authStore.loading,
      error: authStore.error
    };
  }
};
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 70vh;
  padding: 20px;
  background: linear-gradient(135deg, rgba(0, 86, 179, 0.03) 0%, rgba(0, 173, 239, 0.03) 100%);
}

.register-form {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.register-form h2 {
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
}

.register-button {
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

.register-button:hover:not(:disabled) {
  background: linear-gradient(45deg, #004085, #0056b3);
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 86, 179, 0.3);
}

.register-button:active {
  transform: translateY(0);
}

.register-button:disabled {
  background: #6c757d;
  cursor: not-allowed;
  transform: none;
}

.login-link {
  text-align: center;
  margin-top: 20px;
  color: #666;
}

.login-link a {
  color: #0056b3;
  text-decoration: none;
  transition: color 0.3s ease;
}

.login-link a:hover {
  color: #004085;
  text-decoration: underline;
}
</style>