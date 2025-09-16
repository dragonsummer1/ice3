<template>
  <div class="hot-comments">
    <div class="page-header">
      <h2>热门评论</h2>
      <div class="header-info">
        <span>展示最近一周内收到互动最多的评论</span>
      </div>
    </div>

    <div class="filter-section">
      <el-select v-model="categoryFilter" placeholder="按话题分类筛选" @change="loadComments">
        <el-option label="全部分类" value=""></el-option>
        <el-option v-for="category in categories" :key="category" :label="category" :value="category"></el-option>
      </el-select>
      
      <el-select v-model="timeFilter" placeholder="时间范围" @change="loadComments">
        <el-option label="最近一周" value="7"></el-option>
        <el-option label="最近一个月" value="30"></el-option>
        <el-option label="最近三个月" value="90"></el-option>
        <el-option label="全部时间" value=""></el-option>
      </el-select>
    </div>

    <div class="comments-container">
      <el-card 
        v-for="comment in hotComments" 
        :key="comment.id"
        class="comment-card"
      >
        <template #header>
          <div class="comment-header">
            <div class="comment-user-info">
              <span class="user-avatar">
                <el-icon><User /></el-icon>
              </span>
              <span class="username">{{ comment.author.username }}</span>
              <span class="comment-time">{{ formatDate(comment.created_at) }}</span>
            </div>
            <div class="comment-stats">
              <el-tag type="primary" size="small">
                <el-icon><Star /></el-icon> {{ comment.likes || 0 }} 赞
              </el-tag>
            </div>
          </div>
        </template>
        
        <div class="comment-content">
          {{ comment.content }}
        </div>
        
        <div class="comment-topic">
          <el-divider>所属话题</el-divider>
          <router-link :to="`/forum/topic/${comment.topic_id}`" class="topic-link">
            <el-icon><Message /></el-icon> {{ comment.topic_title }}
          </router-link>
        </div>
      </el-card>
    </div>

    <div v-if="loading" class="loading-container">
      <el-loading v-loading="loading" element-loading-text="加载中..." element-loading-spinner="el-icon-loading" element-loading-background="rgba(0, 0, 0, 0.8)">
        <div style="min-height: 400px;"></div>
      </el-loading>
    </div>

    <div v-else-if="hotComments.length === 0" class="empty-container">
      <el-empty description="暂无热门评论"></el-empty>
    </div>
  </div>
</template>

<script>
import { onMounted, ref, reactive } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { User, Star, Message } from '@element-plus/icons-vue';

const CATEGORIES = ['交通', '景点', '住宿', '美食', '购物', '其他'];

export default {
  name: 'HotCommentsView',
  components: {
    User,
    Star,
    Message
  },
  setup() {
    const loading = ref(false);
    const hotComments = ref([]);
    const categoryFilter = ref('');
    const timeFilter = ref('7');
    const categories = CATEGORIES;

    // 格式化日期
    const formatDate = (dateString) => {
      const date = new Date(dateString);
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      });
    };

    // 加载热门评论
    const loadComments = async () => {
      loading.value = true;
      try {
        const params = {};
        
        if (categoryFilter.value) {
          params.category = categoryFilter.value;
        }
        
        if (timeFilter.value) {
          params.days = timeFilter.value;
        }

        const response = await axios.get('/api/forum/hot-comments', { params });
        // 为每个评论添加话题标题
        const commentsWithTopicInfo = await Promise.all(
          response.data.comments.map(async (comment) => {
            if (comment.topic_id) {
              try {
                const topicResponse = await axios.get(`/api/forum/topics/${comment.topic_id}`);
                comment.topic_title = topicResponse.data.title;
              } catch (error) {
                comment.topic_title = '话题已删除';
              }
            } else {
              comment.topic_title = '无主题评论';
            }
            return comment;
          })
        );

        hotComments.value = commentsWithTopicInfo;
      } catch (error) {
        console.error('加载热门评论失败:', error);
        ElMessage.error('加载热门评论失败');
      } finally {
        loading.value = false;
      }
    };

    // 组件挂载时加载数据
    onMounted(() => {
      loadComments();
    });

    return {
      loading,
      hotComments,
      categoryFilter,
      timeFilter,
      categories,
      formatDate,
      loadComments
    };
  }
};
</script>

<style scoped>
.hot-comments {
  padding: 20px;
  max-width: 1000px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e4e7ed;
}

.header-info {
  color: #909399;
  margin-top: 5px;
}

.filter-section {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}

.filter-section .el-select {
  width: 180px;
}

.comments-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(450px, 1fr));
  gap: 20px;
}

.comment-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.comment-user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-avatar {
  width: 32px;
  height: 32px;
  background-color: #1890ff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.username {
  font-weight: bold;
  color: #303133;
}

.comment-time {
  color: #909399;
  font-size: 12px;
}

.comment-stats {
  display: flex;
  align-items: center;
  gap: 10px;
}

.comment-content {
  padding: 15px 0;
  line-height: 1.6;
  word-break: break-word;
  flex: 1;
}

.comment-topic {
  margin-top: 10px;
}

.topic-link {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #1890ff;
  text-decoration: none;
  padding: 10px 0;
}

.topic-link:hover {
  text-decoration: underline;
}

.loading-container,
.empty-container {
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>