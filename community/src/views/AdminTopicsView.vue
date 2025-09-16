<template>
  <el-card class="topics-container">
    <template #header>
      <div class="topics-header">
        <h1>话题管理</h1>
        <el-input
          v-model="searchQuery"
          placeholder="搜索话题标题或内容..."
          prefix-icon="Search"
          style="width: 300px;"
          @input="handleSearch"
        />
      </div>
    </template>
    
    <!-- 话题表格 -->
    <el-table
      :data="filteredTopics"
      style="width: 100%"
      stripe
      border
      :loading="loading"
      empty-text="暂无话题数据"
      v-loading="loading"
    >
      <el-table-column prop="id" label="ID" width="80" type="index"></el-table-column>
      <el-table-column prop="title" label="标题" width="300">
        <template #default="scope">
          <el-tooltip :content="scope.row.content" placement="top" effect="dark" :disabled="scope.row.content.length < 50">
            <span class="topic-title">{{ scope.row.title }}</span>
          </el-tooltip>
        </template>
      </el-table-column>
      <el-table-column prop="user.username" label="作者" width="120">
        <template #default="scope">
          {{ scope.row.user?.username || '未知' }}
        </template>
      </el-table-column>
      <el-table-column prop="category" label="分类" width="100"></el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template #default="scope">
          {{ formatDate(scope.row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="100">
        <template #default="scope">
          <el-tag :type="getStatusType(scope.row.status)">
            {{ getStatusText(scope.row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180" fixed="right">
        <template #default="scope">
          <el-button 
            :type="scope.row.status === 'published' ? 'warning' : 'success'" 
            size="small" 
            @click="toggleTopicStatus(scope.row)"
            :loading="updatingTopicId === scope.row.id"
          >
            {{ scope.row.status === 'published' ? '屏蔽' : '发布' }}
          </el-button>
          <el-button 
            type="danger" 
            size="small" 
            @click="confirmDelete(scope.row)"
            :loading="deletingTopicId === scope.row.id"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

<script>
import { useAdminStore } from '../stores/admin.js';
import { onMounted, ref, computed } from 'vue';
import { Search } from '@element-plus/icons-vue';
import { ElMessage, ElMessageBox } from 'element-plus';

export default {
  name: 'AdminTopicsView',
  components: {
    Search
  },
  setup() {
    const adminStore = useAdminStore();
    const searchQuery = ref('');
    const updatingTopicId = ref(null);
    const deletingTopicId = ref(null);
    
    // 加载话题列表
    onMounted(() => {
      loadTopics();
    });
    
    const loadTopics = async () => {
      try {
        await adminStore.getTopics();
      } catch (error) {
        console.error('Failed to load topics:', error);
        ElMessage.error('加载话题列表失败');
      }
    };
    
    // 搜索话题
    const handleSearch = () => {
      // 搜索逻辑在computed中处理
    };
    
    // 格式化日期
    const formatDate = (dateString) => {
      const date = new Date(dateString);
      return new Intl.DateTimeFormat('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date);
    };
    
    // 获取状态文本
    const getStatusText = (status) => {
      const statusMap = {
        'pending': '待审核',
        'published': '已发布',
        'blocked': '已屏蔽'
      };
      return statusMap[status] || status;
    };
    
    // 获取状态对应的标签类型
    const getStatusType = (status) => {
      const typeMap = {
        'pending': 'warning',
        'published': 'success',
        'blocked': 'danger'
      };
      return typeMap[status] || 'default';
    };
    
    // 切换话题状态
    const toggleTopicStatus = async (topic) => {
      try {
        updatingTopicId.value = topic.id;
        const newStatus = topic.status === 'published' ? 'blocked' : 'published';
        await adminStore.updateTopicStatus(topic.id, newStatus);
        await loadTopics();
        ElMessage.success(`话题已${newStatus === 'published' ? '发布' : '屏蔽'}`);
      } catch (error) {
        console.error('Failed to update topic status:', error);
        ElMessage.error(`切换话题状态失败`);
      } finally {
        updatingTopicId.value = null;
      }
    };
    
    // 确认删除话题
    const confirmDelete = async (topic) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除话题 "${topic.title}" 吗？此操作不可撤销。`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        );
        await handleDeleteTopic(topic.id);
      } catch (error) {
        // 用户取消删除操作
        if (error !== 'cancel') {
          console.error('Delete confirmation failed:', error);
        }
      }
    };
    
    // 删除话题
    const handleDeleteTopic = async (topicId) => {
      try {
        deletingTopicId.value = topicId;
        await adminStore.deleteTopic(topicId);
        await loadTopics();
        ElMessage.success('话题已删除');
      } catch (error) {
        console.error('Failed to delete topic:', error);
        ElMessage.error('删除话题失败');
      } finally {
        deletingTopicId.value = null;
      }
    };
    
    // 过滤话题列表
    const filteredTopics = computed(() => {
      if (!searchQuery.value) return adminStore.topics;
      
      const query = searchQuery.value.toLowerCase();
      return adminStore.topics.filter(topic => 
        topic.title.toLowerCase().includes(query) ||
        topic.content.toLowerCase().includes(query)
      );
    });
    
    return {
      searchQuery,
      topics: adminStore.topics,
      loading: adminStore.loading,
      updatingTopicId,
      deletingTopicId,
      handleSearch,
      formatDate,
      getStatusText,
      getStatusType,
      toggleTopicStatus,
      confirmDelete,
      filteredTopics
    };
  }
};
</script>

<style scoped>
.topics-container {
  margin: 20px;
}

.topics-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.topics-header h1 {
  margin: 0;
  color: #333;
  font-size: 20px;
  font-weight: 600;
}

.topic-title {
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.el-table .el-button + .el-button {
  margin-left: 10px;
}
</style>