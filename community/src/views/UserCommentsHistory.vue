<template>
  <div class="user-comments-history">
    <div class="page-header">
      <h2>我的评论历史</h2>
      <div class="header-actions">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索评论内容"
          style="width: 300px;"
          suffix-icon="el-icon-search"
          @keyup.enter="loadComments"
        />
        <el-button 
          type="primary" 
          style="margin-left: 10px;"
          @click="loadComments"
        >
          搜索
        </el-button>
      </div>
    </div>

    <el-table
      v-loading="loading"
      :data="commentsData"
      style="width: 100%"
      border
    >
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="content" label="评论内容" min-width="400">
        <template #default="scope">
          <div class="comment-content">{{ scope.row.content }}</div>
        </template>
      </el-table-column>
      <el-table-column prop="topic_title" label="所属话题" width="200">
        <template #default="scope">
          <router-link 
            :to="`/forum/topic/${scope.row.topic_id}`"
            class="topic-link"
            target="_blank"
          >
            {{ scope.row.topic_title }}
          </router-link>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="发表时间" width="180">
        <template #default="scope">
          {{ formatDate(scope.row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="100">
        <template #default="scope">
          <el-tag :type="getStatusTagType(scope.row.status)">
            {{ getStatusText(scope.row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="100" fixed="right">
        <template #default="scope">
          <el-button
            v-if="scope.row.status !== 'deleted'"
            type="danger"
            size="small"
            @click="handleDelete(scope.row)"
          >
            删除
          </el-button>
          <el-button
            v-else
            type="info"
            size="small"
            disabled
          >
            已删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination-container">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="totalComments"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script>
import { onMounted, ref, computed } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { useAuthStore } from '../stores/auth.js';
import { useForumStore } from '../stores/forum.js';

export default {
  name: 'UserCommentsHistory',
  setup() {
    const loading = ref(false);
    const comments = ref([]);
    const totalComments = ref(0);
    const currentPage = ref(1);
    const pageSize = ref(20);
    const searchKeyword = ref('');
    const authStore = useAuthStore();
    const forumStore = useForumStore();
    const allComments = ref([]); // 存储所有评论，用于搜索

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

    // 获取状态标签类型
    const getStatusTagType = (status) => {
      switch (status) {
        case 'approved':
          return 'success';
        case 'pending':
          return 'warning';
        case 'deleted':
          return 'danger';
        default:
          return 'info';
      }
    };

    // 获取状态文本
    const getStatusText = (status) => {
      switch (status) {
        case 'approved':
          return '已批准';
        case 'pending':
          return '待审核';
        case 'deleted':
          return '已删除';
        default:
          return status;
      }
    };

    // 加载评论列表
    const loadComments = async () => {
      if (!authStore.isAuthenticated) {
        ElMessage.warning('请先登录');
        return;
      }

      loading.value = true;
      try {
        const params = {
          page: currentPage.value,
          per_page: pageSize.value
        };

        if (searchKeyword.value) {
          params.search = searchKeyword.value;
        }

        const response = await forumStore.getUserComments(params);
        comments.value = response.comments;
        allComments.value = [...response.comments]; // 保存原始数据用于搜索
        totalComments.value = response.total || 0;
      } catch (error) {
        console.error('加载评论失败:', error);
        ElMessage.error(forumStore.error || '加载评论失败');
      } finally {
        loading.value = false;
      }
    };

    // 处理页面大小变化
    const handleSizeChange = (size) => {
      pageSize.value = size;
      loadComments();
    };

    // 处理当前页面变化
    const handleCurrentChange = (current) => {
      currentPage.value = current;
      loadComments();
    };

    // 删除评论
    const handleDelete = async (comment) => {
      ElMessageBox.confirm('确定要删除这条评论吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          await forumStore.deleteComment(comment.id);
          // 从本地列表中移除
          comments.value = comments.value.filter(c => c.id !== comment.id);
          allComments.value = allComments.value.filter(c => c.id !== comment.id);
          totalComments.value = Math.max(0, totalComments.value - 1);
          ElMessage.success('评论已删除');
        } catch (error) {
          console.error('删除评论失败:', error);
          ElMessage.error(forumStore.error || '删除评论失败');
        }
      }).catch(() => {
        // 用户取消删除
      });
    };

    // 组件挂载时加载数据
    onMounted(() => {
      loadComments();
    });

    // 计算评论数据
    const commentsData = computed(() => {
      return comments.value;
    });

    // 搜索评论
    const searchComments = () => {
      if (searchKeyword.value.trim()) {
        const filteredComments = allComments.value.filter(comment => 
          comment.content.includes(searchKeyword.value.trim())
        );
        comments.value = filteredComments;
      } else {
        comments.value = [...allComments.value];
      }
    };
    
    // 清除搜索
    const clearSearch = () => {
      searchKeyword.value = '';
      comments.value = [...allComments.value];
    };

    return {
      loading,
      commentsData,
      totalComments,
      currentPage,
      pageSize,
      searchKeyword,
      formatDate,
      getStatusTagType,
      getStatusText,
      loadComments,
      handleSizeChange,
      handleCurrentChange,
      handleDelete,
      searchComments,
      clearSearch
    };
  }
};
</script>

<style scoped>
.user-comments-history {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e4e7ed;
}

.header-actions {
  display: flex;
  align-items: center;
}

.comment-content {
  word-break: break-word;
  line-height: 1.5;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.topic-link {
  color: #1890ff;
  text-decoration: none;
}

.topic-link:hover {
  text-decoration: underline;
}
</style>