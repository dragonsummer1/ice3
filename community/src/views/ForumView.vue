<template>
  <div class="forum">
    <div class="container">
      <h2>哈尔滨旅游论坛</h2>
      
      <div class="forum-header">
        <div class="forum-stats">
          <p>今日话题: <span>{{ todayTopics }}</span></p>
          <p>在线用户: <span>{{ onlineUsers }}</span></p>
        </div>
        <button class="new-topic-btn" @click="showNewTopicForm = true">发布新话题</button>
      </div>
      
      <!-- 发布新话题弹窗 -->
      <div v-if="showNewTopicForm" class="modal-overlay" @click.self="showNewTopicForm = false">
        <div class="modal">
          <h3>发布新话题</h3>
          <div class="form-group">
            <label for="topic-title">标题</label>
            <input type="text" id="topic-title" v-model="newTopic.title" placeholder="请输入话题标题">
          </div>
          <div class="form-group">
            <label for="topic-category">分类</label>
            <select id="topic-category" v-model="newTopic.category">
              <option value="">请选择分类</option>
              <option value="攻略分享">攻略分享</option>
              <option value="结伴同行">结伴同行</option>
              <option value="景点讨论">景点讨论</option>
              <option value="美食推荐">美食推荐</option>
              <option value="住宿咨询">住宿咨询</option>
              <option value="交通出行">交通出行</option>
              <option value="其他">其他</option>
            </select>
          </div>
          <div class="form-group">
            <label for="topic-content">内容</label>
            <textarea id="topic-content" v-model="newTopic.content" placeholder="请输入话题内容..." rows="6"></textarea>
          </div>
          <div class="modal-actions">
            <button @click="showNewTopicForm = false">取消</button>
            <button @click="publishTopic" class="primary">发布</button>
          </div>
        </div>
      </div>
      
      <div class="forum-content">
        <div class="forum-sidebar">
          <div class="category-list">
            <h3>话题分类</h3>
            <ul>
              <li 
                v-for="category in categories" 
                :key="category.id"
                :class="{ active: selectedCategory === category.id }"
                @click="selectedCategory = category.id"
              >
                <span class="category-name">{{ category.name }}</span>
                <span class="category-count">({{ category.count }})</span>
              </li>
            </ul>
          </div>
          
          <div class="hot-topics">
            <h3>热门话题</h3>
            <ul>
              <li v-for="topic in hotTopics" :key="topic.id">
                <a href="#" @click.prevent="viewTopic(topic.id)">{{ topic.title }}</a>
              </li>
            </ul>
          </div>
        </div>
        
        <div class="forum-main">
          <div class="topic-list">
            <div class="topic-header-row">
              <div class="topic-title-col">标题</div>
              <div class="topic-author-col">作者</div>
              <div class="topic-replies-col">回复</div>
              <div class="topic-views-col">浏览</div>
              <div class="topic-time-col">最后回复</div>
            </div>
            
            <div 
              v-for="topic in filteredTopics" 
              :key="topic.id" 
              class="topic-item"
              @click="viewTopic(topic.id)"
            >
              <div class="topic-title-col">
                <div class="topic-title">
                  <span class="topic-tag" v-if="topic.tag">{{ topic.tag }}</span>
                  {{ topic.title }}
                </div>
              </div>
              <div class="topic-author-col">
                <div class="author-info">
                  <span class="author-avatar">{{ topic.author.substring(0, 1) }}</span>
                  <span class="author-name">{{ topic.author }}</span>
                </div>
              </div>
              <div class="topic-replies-col">{{ topic.replies }}</div>
              <div class="topic-views-col">{{ topic.views }}</div>
              <div class="topic-time-col">{{ topic.lastReplyTime }}</div>
            </div>
          </div>
          
          <!-- 分页 -->
          <div class="pagination">
            <button 
              v-for="page in totalPages" 
              :key="page"
              :class="{ active: currentPage === page }"
              @click="currentPage = page"
            >
              {{ page }}
            </button>
          </div>
        </div>
      </div>
      
      <!-- 话题详情弹窗 -->
      <div v-if="selectedTopic" class="modal-overlay" @click.self="closeTopicDetail">
        <div class="topic-detail-modal">
          <div class="topic-detail-header">
            <h3>{{ selectedTopic.title }}</h3>
            <button class="close-btn" @click="closeTopicDetail">×</button>
          </div>
          
          <div class="topic-detail-info">
            <span class="topic-detail-author">{{ selectedTopic.author }}</span>
            <span class="topic-detail-time">{{ selectedTopic.time }}</span>
            <span class="topic-detail-views">浏览: {{ selectedTopic.views }}</span>
          </div>
          
          <div class="topic-detail-content">
            {{ selectedTopic.content }}
          </div>
          
          <div class="topic-detail-replies">
            <h4>回复 ({{ selectedTopic.replies }})</h4>
            <div v-for="reply in selectedTopic.replyList" :key="reply.id" class="reply-item">
              <div class="reply-header">
                <span class="reply-author">{{ reply.author }}</span>
                <span class="reply-time">{{ reply.time }}</span>
              </div>
              <div class="reply-content">{{ reply.content }}</div>
            </div>
          </div>
          
          <div class="topic-detail-reply-form">
            <h4>发表回复</h4>
            <textarea v-model="replyContent" placeholder="请输入回复内容..." rows="3"></textarea>
            <button @click="submitReply" class="primary">回复</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth.js';
import { useRouter } from 'vue-router';
import { useForumStore } from '../stores/forum.js';

export default {
  name: 'ForumView',
  data() {
    const authStore = useAuthStore();
    const router = useRouter();
    const forumStore = useForumStore();
    
    return {
      authStore,
      router,
      forumStore,
      todayTopics: 128,
      onlineUsers: 342,
      showNewTopicForm: false,
      newTopic: {
        title: '',
        category: '',
        content: ''
      },
      categories: [
        { id: 'all', name: '全部', count: 1250 },
        { id: 'guides', name: '攻略分享', count: 320 },
        { id: 'companions', name: '结伴同行', count: 180 },
        { id: 'attractions', name: '景点讨论', count: 250 },
        { id: 'food', name: '美食推荐', count: 150 },
        { id: 'accommodation', name: '住宿咨询', count: 120 },
        { id: 'transport', name: '交通出行', count: 80 },
        { id: 'other', name: '其他', count: 50 }
      ],
      selectedCategory: 'all',
      selectedTopic: null,
      replyContent: '',
      currentPage: 1,
      pageSize: 10
    }
  },
  async mounted() {
    // 额外检查用户是否已登录，如果未登录则重定向到登录页
    if (!this.authStore.isAuthenticated) {
      this.router.push('/login');
      return;
    }
    
    // 初始化时从后端获取话题列表
    try {
      await this.forumStore.getTopics();
    } catch (error) {
      console.error('获取话题列表失败:', error);
    }
    
    // 添加滚动事件监听
    window.addEventListener('scroll', this.animateOnScroll);
    // 初始化时执行一次，确保可视区域内的元素也能被动画化
    this.animateOnScroll();
  },
  computed: {
    // 从forumStore获取话题数据，确保实时更新
    topics() {
      return this.forumStore.topics || []
    },
    
    filteredTopics() {
      if (this.selectedCategory === 'all') {
        return this.topics
      }
      return this.topics.filter(topic => topic.category === this.selectedCategory)
    },
    
    totalPages() {
      return Math.ceil(this.filteredTopics.length / this.pageSize)
    },
    
    hotTopics() {
      // 简单地取前5个回复最多的话题作为热门话题
      return [...this.topics]
        .sort((a, b) => b.replies - a.replies)
        .slice(0, 5)
    }
  },
  methods: {
    async publishTopic() {
      if (this.newTopic.title && this.newTopic.content && this.newTopic.category) {
        try {
          // 调用后端API发布话题
          await this.forumStore.createTopic(this.newTopic);
          
          // 如果API调用成功，更新前端视图
          const now = new Date()
          const formattedTime = now.getFullYear() + '-' + 
                               String(now.getMonth() + 1).padStart(2, '0') + '-' + 
                               String(now.getDate()).padStart(2, '0') + ' ' + 
                               String(now.getHours()).padStart(2, '0') + ':' + 
                               String(now.getMinutes()).padStart(2, '0')
          
          const newTopicObj = {
            id: Date.now(),
            title: this.newTopic.title,
            author: this.authStore.user?.username || '匿名用户',
            authorAvatar: this.authStore.user?.username?.substring(0, 1) || '匿',
            tag: '',
            replies: 0,
            views: 0,
            time: formattedTime,
            lastReplyTime: formattedTime,
            category: this.newTopic.category,
            content: this.newTopic.content,
            replyList: []
          }
          
          this.topics.unshift(newTopicObj)
          
          // 重置表单
          this.newTopic = {
            title: '',
            category: '',
            content: ''
          }
          
          this.showNewTopicForm = false
          alert('话题发布成功！')
        } catch (error) {
          console.error('发布话题失败:', error)
          alert('发布话题失败，请稍后重试')
        }
      } else {
        alert('请填写完整的话题信息')
      }
    },
    async viewTopic(topicId) {
      try {
        // 从服务器获取最新的话题数据（包含已批准评论）
        const topic = await this.forumStore.getTopic(topicId);
        
        // 处理话题数据和评论数据
        this.selectedTopic = {
          ...topic,
          // 重命名comments为replyList以保持与现有前端代码兼容
          replyList: topic.comments || []
        };
        this.replyContent = '';
      } catch (error) {
        console.error('获取话题详情失败:', error);
        alert('获取话题详情失败，请稍后重试');
      }
    },
    closeTopicDetail() {
      this.selectedTopic = null
    },
    async submitReply() {
      if (this.replyContent.trim() && this.selectedTopic) {
        try {
          // 调用后端API提交评论
          await this.forumStore.createReply(this.selectedTopic.id, this.replyContent);
          
          // 如果API调用成功，更新前端视图
          const now = new Date()
          const formattedTime = now.getFullYear() + '-' + 
                               String(now.getMonth() + 1).padStart(2, '0') + '-' + 
                               String(now.getDate()).padStart(2, '0') + ' ' + 
                               String(now.getHours()).padStart(2, '0') + ':' + 
                               String(now.getMinutes()).padStart(2, '0')
          
          const newReply = {
            id: Date.now(),
            author: this.authStore.user?.username || '匿名用户',
            time: formattedTime,
            content: this.replyContent
          }
          
          // 更新选中的话题
          this.selectedTopic.replyList.push(newReply)
          this.selectedTopic.replies++
          this.selectedTopic.lastReplyTime = formattedTime
          
          // 更新原话题数据
          const originalTopic = this.topics.find(t => t.id === this.selectedTopic.id)
          if (originalTopic) {
            originalTopic.replyList.push(newReply)
            originalTopic.replies++
            originalTopic.lastReplyTime = formattedTime
          }
          
          this.replyContent = ''
          alert('评论已提交，等待管理员审核！')
        } catch (error) {
          console.error('发表评论失败:', error)
          alert('发表评论失败，请稍后重试')
        }
      } else {
        alert('请输入回复内容')
      }
    },
    // 滚动触发动画
    animateOnScroll() {
      const elements = document.querySelectorAll('.forum-header, .forum-sidebar, .forum-main, .topic-item, .hot-topics li, .category-list li')
      elements.forEach(element => {
        const position = element.getBoundingClientRect()
        // 元素进入视口
        if (position.top < window.innerHeight - 100 && position.bottom >= 0) {
          element.classList.add('fade-in-up')
        }
      })
    }
  },

  beforeUnmount() {
    // 清理事件监听器
    window.removeEventListener('scroll', this.animateOnScroll)
  }
}
</script>

<style scoped>
/* 导入全局动画样式 */
@import '../assets/animations.css';

.forum {
  padding: 30px 0;
  position: relative;
  overflow: hidden;
}

/* 背景装饰 */
.forum::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(0, 86, 179, 0.03) 0%, rgba(0, 173, 239, 0.03) 100%);
  z-index: -1;
}

.forum h2 {
  text-align: center;
  font-size: 2.2rem;
  margin-bottom: 30px;
  color: #0056b3;
  position: relative;
  display: inline-block;
  left: 50%;
  transform: translateX(-50%);
}

/* 标题装饰线 */
.forum h2::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, transparent, #0056b3, transparent);
  border-radius: 2px;
}

.forum-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  padding: 15px 20px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  border: 1px solid rgba(255, 255, 255, 0.5);
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}

.forum-stats {
  display: flex;
  gap: 30px;
}

.forum-stats p {
  margin: 0;
  color: #666;
  font-size: 1.05rem;
}

.forum-stats span {
  color: #0056b3;
  font-weight: bold;
  font-size: 1.1rem;
}

.new-topic-btn {
  padding: 12px 24px;
  background: linear-gradient(45deg, #0056b3, #007bff);
  color: white;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1rem;
  font-weight: 500;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 86, 179, 0.2);
}

/* 按钮悬停效果 */
.new-topic-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 86, 179, 0.3);
}

/* 按钮伪元素动画 */
.new-topic-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.5s;
}

.new-topic-btn:hover::before {
  left: 100%;
}

.forum-content {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  justify-content: center;
}

.forum-sidebar {
  flex: 0 0 280px;
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.8s ease, transform 0.8s ease;
}

.forum-main {
  flex: 1;
  min-width: 600px;
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.8s ease, transform 0.8s ease;
}

.category-list,
.hot-topics {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  padding: 25px;
  margin-bottom: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  border: 1px solid rgba(255, 255, 255, 0.5);
  position: relative;
  overflow: hidden;
}

.category-list h3,
.hot-topics h3 {
  font-size: 1.3rem;
  margin-bottom: 15px;
  color: #0056b3;
  position: relative;
  padding-bottom: 10px;
}

.category-list h3::after,
.hot-topics h3::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 40px;
  height: 3px;
  background: linear-gradient(90deg, #0056b3, #007bff);
  border-radius: 1.5px;
}

.category-list ul,
.hot-topics ul {
  list-style: none;
  padding: 0;
}

.category-list li {
  padding: 12px 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 8px;
  margin-bottom: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.7);
  opacity: 0;
  transform: translateY(10px);
  transition: opacity 0.4s ease, transform 0.4s ease, all 0.3s ease;
}

.category-list li:hover {
  background: linear-gradient(135deg, #0056b3, #007bff);
  color: white;
  transform: translateX(5px);
  box-shadow: 0 4px 12px rgba(0, 86, 179, 0.3);
}

.category-list li.active {
  background: linear-gradient(135deg, #0056b3, #007bff);
  color: white;
  box-shadow: 0 4px 12px rgba(0, 86, 179, 0.3);
}

.category-count {
  font-size: 0.9rem;
  opacity: 0.8;
}

.hot-topics li {
  margin-bottom: 12px;
  opacity: 0;
  transform: translateY(10px);
  transition: opacity 0.4s ease, transform 0.4s ease;
}

.hot-topics a {
  color: #333;
  text-decoration: none;
  transition: all 0.3s ease;
  display: block;
  padding: 8px 12px;
  border-radius: 6px;
  position: relative;
  overflow: hidden;
}

.hot-topics a:hover {
  color: #0056b3;
  background: rgba(0, 86, 179, 0.05);
  transform: translateX(5px);
}

/* 热门话题链接装饰 */
.hot-topics a::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  width: 4px;
  height: 100%;
  background: linear-gradient(to bottom, #0056b3, #007bff);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.hot-topics a:hover::before {
  opacity: 1;
}

.topic-list {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.5);
}

.topic-header-row {
  display: grid;
  grid-template-columns: 1fr 120px 80px 80px 120px;
  padding: 15px 20px;
  background: linear-gradient(135deg, #0056b3, #007bff);
  color: white;
  font-weight: bold;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.topic-item {
  display: grid;
  grid-template-columns: 1fr 120px 80px 80px 120px;
  padding: 15px 20px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.7);
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s ease, transform 0.6s ease, all 0.3s ease;
}

.topic-item:hover {
  background: white;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.1);
}

.topic-item:last-child {
  border-bottom: none;
}

.topic-title {
  font-weight: bold;
  color: #0056b3;
  font-size: 1.05rem;
  transition: color 0.3s ease;
}

.topic-item:hover .topic-title {
  color: #007bff;
}

.topic-tag {
  display: inline-block;
  padding: 2px 10px;
  background: linear-gradient(135deg, #0056b3, #007bff);
  color: white;
  font-size: 0.8rem;
  border-radius: 15px;
  margin-right: 8px;
  box-shadow: 0 2px 6px rgba(0, 86, 179, 0.2);
}

.author-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.author-avatar {
  display: inline-block;
  width: 30px;
  height: 30px;
  background: linear-gradient(135deg, #0056b3, #007bff);
  color: white;
  border-radius: 50%;
  text-align: center;
  line-height: 30px;
  font-size: 0.9rem;
  box-shadow: 0 2px 6px rgba(0, 86, 179, 0.3);
}

.author-name {
  font-size: 0.9rem;
  color: #666;
  font-weight: 500;
}

.topic-replies-col,
.topic-views-col {
  color: #666;
  font-size: 0.9rem;
  font-weight: 500;
}

.topic-time-col {
  color: #999;
  font-size: 0.8rem;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  padding: 10px;
}

.pagination button {
  padding: 8px 16px;
  margin: 0 5px;
  border: 1px solid #ddd;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 20px;
  font-weight: 500;
}

.pagination button:hover {
  background: linear-gradient(135deg, #0056b3, #007bff);
  color: white;
  border-color: #0056b3;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 86, 179, 0.3);
}

.pagination button.active {
  background: linear-gradient(135deg, #0056b3, #007bff);
  color: white;
  border-color: #0056b3;
  box-shadow: 0 4px 12px rgba(0, 86, 179, 0.3);
}

/* 弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease-out;
}

.modal {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  padding: 30px;
  border-radius: 16px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.8);
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.modal h3 {
  margin-bottom: 20px;
  color: #0056b3;
  position: relative;
  padding-bottom: 10px;
}

.modal h3::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 50px;
  height: 3px;
  background: linear-gradient(90deg, #0056b3, #007bff);
  border-radius: 1.5px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-weight: bold;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.8);
  transition: all 0.3s ease;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #0056b3;
  box-shadow: 0 0 0 3px rgba(0, 86, 179, 0.1);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 30px;
}

.modal-actions button {
  padding: 10px 20px;
  border: 1px solid #ddd;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 25px;
  font-weight: 500;
}

.modal-actions button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.modal-actions button.primary {
  background: linear-gradient(45deg, #0056b3, #007bff);
  color: white;
  border-color: #0056b3;
}

.modal-actions button.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 86, 179, 0.3);
}

/* 话题详情弹窗 */
.topic-detail-modal {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  padding: 30px;
  border-radius: 16px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.8);
  animation: slideIn 0.3s ease-out;
}

.topic-detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.topic-detail-header h3 {
  margin: 0;
  color: #0056b3;
  font-size: 1.5rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #999;
  transition: all 0.3s ease;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.close-btn:hover {
  color: #333;
  background: rgba(0, 0, 0, 0.05);
  transform: rotate(90deg);
}

.topic-detail-info {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.topic-detail-author {
  font-weight: bold;
  color: #0056b3;
  font-size: 1.05rem;
}

.topic-detail-time,
.topic-detail-views {
  color: #999;
  font-size: 0.9rem;
}

.topic-detail-content {
  margin-bottom: 30px;
  line-height: 1.8;
  color: #333;
  white-space: pre-wrap;
  background: rgba(255, 255, 255, 0.7);
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.topic-detail-replies h4 {
  margin-bottom: 20px;
  color: #0056b3;
  position: relative;
  padding-bottom: 10px;
}

.topic-detail-replies h4::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 40px;
  height: 3px;
  background: linear-gradient(90deg, #0056b3, #007bff);
  border-radius: 1.5px;
}

.reply-item {
  padding: 20px 0;
  border-bottom: 1px solid #f0f0f0;
  transition: all 0.3s ease;
  position: relative;
}

.reply-item:hover {
  background: rgba(0, 86, 179, 0.03);
  transform: translateX(5px);
}

.reply-item:last-child {
  border-bottom: none;
}

.reply-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.reply-author {
  font-weight: bold;
  color: #0056b3;
}

.reply-time {
  color: #999;
  font-size: 0.9rem;
}

.reply-content {
  color: #666;
  line-height: 1.6;
  background: rgba(255, 255, 255, 0.7);
  padding: 15px;
  border-radius: 8px;
  border-left: 4px solid #0056b3;
}

.topic-detail-reply-form h4 {
  margin-bottom: 10px;
  color: #0056b3;
}

.topic-detail-reply-form textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  resize: vertical;
  margin-bottom: 10px;
  background: rgba(255, 255, 255, 0.8);
  transition: all 0.3s ease;
}

.topic-detail-reply-form textarea:focus {
  outline: none;
  border-color: #0056b3;
  box-shadow: 0 0 0 3px rgba(0, 86, 179, 0.1);
}

.topic-detail-reply-form button {
  padding: 10px 20px;
  background: linear-gradient(45deg, #0056b3, #007bff);
  color: white;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  box-shadow: 0 4px 15px rgba(0, 86, 179, 0.2);
}

.topic-detail-reply-form button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 86, 179, 0.3);
}

@media (max-width: 768px) {
  .forum-content {
    flex-direction: column;
  }
  
  .forum-sidebar {
    flex: none;
    width: 100%;
  }
  
  .forum-main {
    min-width: auto;
  }
  
  .topic-header-row,
  .topic-item {
    grid-template-columns: 1fr 100px;
    grid-template-areas: 
      "title title"
      "author time"
      "replies views";
  }
  
  .topic-title-col {
    grid-area: title;
  }
  
  .topic-author-col {
    grid-area: author;
  }
  
  .topic-replies-col {
    grid-area: replies;
  }
  
  .topic-views-col {
    grid-area: views;
  }
  
  .topic-time-col {
    grid-area: time;
  }
}

/* 滚动条美化 */
.forum ::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.forum ::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.05);
  border-radius: 4px;
}

.forum ::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #0056b3, #007bff);
  border-radius: 4px;
}

.forum ::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #004085, #0056b3);
}

/* 使用全局定义的动画效果 */
.fade-in-up {
  animation: slideInBottom 0.8s ease-out forwards;
}

/* 为元素设置不同的动画延迟 */
.forum-sidebar > div:first-child {
  transition-delay: 0.1s;
}

.forum-sidebar > div:last-child {
  transition-delay: 0.2s;
}

.topic-item:nth-child(1) {
  transition-delay: 0.1s;
}

.topic-item:nth-child(2) {
  transition-delay: 0.2s;
}

.topic-item:nth-child(3) {
  transition-delay: 0.3s;
}

.topic-item:nth-child(4) {
  transition-delay: 0.4s;
}

/* 增强版卡片悬停效果 */
.topic-item {
  position: relative;
  overflow: hidden;
  z-index: 1;
}

.topic-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(0, 86, 179, 0.1), transparent);
  transition: left 0.5s ease;
  z-index: -1;
}

.topic-item:hover::before {
  left: 100%;
}
</style>