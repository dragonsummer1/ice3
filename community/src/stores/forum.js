import { defineStore } from 'pinia';
import axios from 'axios';

export const useForumStore = defineStore('forum', {
  state: () => ({
    topics: [],
    currentTopic: null,
    replies: [],
    loading: false,
    error: null,
    totalPages: 1,
    currentPage: 1,
    categories: ['交通', '景点', '住宿', '美食', '购物', '其他']
  }),
  
  actions: {
    // 获取话题列表
    async getTopics(page = 1, category = '', perPage = 10) {
      this.loading = true;
      this.error = null;
      
      try {
        const params = { page, per_page: perPage };
        if (category) {
          params.category = category;
        }
        
        const response = await axios.get('/api/forum/topics', { params });
        
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
    
    // 获取单个话题详情
    async getTopic(topicId) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axios.get(`/api/forum/topics/${topicId}`);
        this.currentTopic = response.data;
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.message || '获取话题详情失败';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    // 创建新话题
    async createTopic(topicData) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axios.post('/api/forum/topics', topicData);
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.message || '创建话题失败';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    // 更新话题
    async updateTopic(topicId, topicData) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axios.put(`/api/forum/topics/${topicId}`, topicData);
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.message || '更新话题失败';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    // 删除话题
    async deleteTopic(topicId) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axios.delete(`/api/forum/topics/${topicId}`);
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.message || '删除话题失败';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    // 获取话题的回复列表
    async getReplies(topicId) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axios.get(`/api/forum/topics/${topicId}/replies`);
        this.replies = response.data;
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.message || '获取回复列表失败';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    // 创建回复
    async createReply(topicId, content) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axios.post(`/api/forum/topics/${topicId}/replies`, { content });
        // 刷新回复列表
        await this.getReplies(topicId);
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.message || '回复失败';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    // 清除错误信息
    clearError() {
      this.error = null;
    }
  }
});