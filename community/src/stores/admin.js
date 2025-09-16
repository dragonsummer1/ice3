import { defineStore } from 'pinia';
import axios from 'axios';

export const useAdminStore = defineStore('admin', {
  state: () => ({
    users: [],
    topics: [],
    stats: null,
    loading: false,
    error: null,
    totalPages: 1,
    currentPage: 1
  }),
  
  actions: {
    // 获取用户列表
    async getUsers(page = 1, perPage = 20) {
      this.loading = true;
      this.error = null;
      
      try {
        const params = { page, per_page: perPage };
        const response = await axios.get('/api/admin/users', { params });
        
        this.users = response.data.users;
        this.totalPages = response.data.pages;
        this.currentPage = response.data.current_page;
        
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.message || '获取用户列表失败';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    // 获取单个用户详情
    async getUser(userId) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axios.get(`/api/admin/users/${userId}`);
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.message || '获取用户详情失败';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    // 更新用户信息
    async updateUser(userId, userData) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axios.put(`/api/admin/users/${userId}`, userData);
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.message || '更新用户信息失败';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    // 删除用户
    async deleteUser(userId) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axios.delete(`/api/admin/users/${userId}`);
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.message || '删除用户失败';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    // 获取所有话题（包括待审核和已屏蔽的）
    async getTopics(page = 1, perPage = 10, status = '') {
      this.loading = true;
      this.error = null;
      
      try {
        const params = { page, per_page: perPage };
        if (status) {
          params.status = status;
        }
        
        const response = await axios.get('/api/admin/topics/all', { params });
        
        this.topics = response.data.topics;
        this.totalPages = response.data.pages;
        this.currentPage = response.data.current_page;
        
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.message || '获取话题列表失败';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    // 更新话题状态
    async updateTopicStatus(topicId, status) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axios.put(`/api/admin/topics/${topicId}/status`, { status });
        
        // 状态更新成功后，刷新论坛的话题列表，确保已发布的话题能立即显示在前端
        const { useForumStore } = await import('./forum.js');
        const forumStore = useForumStore();
        await forumStore.getTopics();
        
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.message || '更新话题状态失败';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    // 获取统计数据
    async getStats() {
      this.loading = true;
      this.error = null;
      
      try {
        console.log('正在请求统计数据...');
        // 从localStorage获取用户信息
        const userData = localStorage.getItem('user');
        // 从cookie获取JWT令牌
        const getJwtToken = () => {
          const nameEQ = 'access_token_cookie=';
          const ca = document.cookie.split(';');
          for(let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) === ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
          }
          return null;
        };
        
        const jwtToken = getJwtToken();
        console.log('获取的JWT令牌:', jwtToken);
        console.log('用户信息:', userData);
        
        // 设置请求头
        const headers = {};
        if (jwtToken) {
          headers['Authorization'] = `Bearer ${jwtToken}`;
        }
        
        const response = await axios.get('/api/admin/stats', { headers });
        console.log('统计数据请求成功:', response.data);
        this.stats = response.data;
        return response.data;
      } catch (error) {
        console.error('获取统计数据失败:', error);
        console.error('错误详情:', error.response);
        this.error = error.response?.data?.message || '获取统计数据失败';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    // 清除错误信息
    clearError() {
      this.error = null;
    },
    
    // 删除话题
    async deleteTopic(topicId) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axios.delete(`/api/admin/topics/${topicId}`);
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.message || '删除话题失败';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    // 获取评论数据
    async getComments(page = 1, perPage = 10) {
      this.loading = true;
      this.error = null;
      
      try {
        const params = { page, per_page: perPage };
        const response = await axios.get('/api/admin/comments', { params });
        
        this.totalPages = response.data.pages;
        this.currentPage = response.data.current_page;
        
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.message || '获取评论数据失败';
        throw error;
      } finally {
        this.loading = false;
      }
    }
  }
});