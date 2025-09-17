import axios from 'axios';
import { defineStore } from 'pinia';
import { getTabId } from './auth.js';

// 创建包含标签页ID的请求配置
export const createRequestConfig = (config = {}) => {
  const tabId = getTabId();
  const headers = config.headers || {};
  
  return {
    ...config,
    headers: {
      ...headers,
      'X-Tab-Id': tabId
    }
  };
};

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
        const response = await axios.get('/api/admin/users', createRequestConfig({ params }));
        
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
        const response = await axios.get(`/api/admin/users/${userId}`, createRequestConfig());
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
        const response = await axios.put(`/api/admin/users/${userId}`, userData, createRequestConfig());
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
        const response = await axios.delete(`/api/admin/users/${userId}`, createRequestConfig());
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
        
        const response = await axios.get('/api/admin/topics/all', createRequestConfig({ params }));
        
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
        const response = await axios.put(`/api/admin/topics/${topicId}/status`, { status }, createRequestConfig());
        
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
        const response = await axios.get('/api/admin/stats', createRequestConfig());
        this.stats = response.data;
        return response.data;
      } catch (error) {
        console.error('获取统计数据失败:', error);
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
        const response = await axios.delete(`/api/admin/topics/${topicId}`, createRequestConfig());
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
        const response = await axios.get('/api/admin/comments', createRequestConfig({ params }));
        
        this.totalPages = response.data.pages;
        this.currentPage = response.data.current_page;
        
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.message || '获取评论数据失败';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    // 更新评论状态
    async updateCommentStatus(commentId, status) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axios.put(
          `/api/admin/comments/${commentId}/${status === 'approved' ? 'approve' : 'reject'}`,
          {},
          createRequestConfig()
        );
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.message || '更新评论状态失败';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    // 删除评论
    async deleteComment(commentId) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axios.delete(
          `/api/admin/comments/${commentId}`,
          createRequestConfig()
        );
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.message || '删除评论失败';
        throw error;
      } finally {
        this.loading = false;
      }
    }
  }
});