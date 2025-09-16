<template>
  <div class="admin-comments">
    <div class="page-header">
      <h2>评论管理</h2>
      <div class="header-actions">
        <el-select v-model="statusFilter" placeholder="按状态筛选">
          <el-option label="全部" value=""></el-option>
          <el-option label="已批准" value="approved"></el-option>
          <el-option label="待审核" value="pending"></el-option>
          <el-option label="已删除" value="deleted"></el-option>
        </el-select>
        <el-input
          v-model="searchKeyword"
          placeholder="搜索评论内容"
          style="width: 300px; margin-left: 20px;"
          suffix-icon="el-icon-search"
        />
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
      <el-table-column prop="author.username" label="评论用户" width="120" />
      <el-table-column prop="created_at" label="创建时间" width="180">
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
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="scope">
          <el-button
            v-if="scope.row.status !== 'approved'"
            type="primary"
            size="small"
            @click="handleApprove(scope.row)"
          >
            批准
          </el-button>
          <el-button
            v-else
            type="warning"
            size="small"
            @click="handleReject(scope.row)"
          >
            驳回
          </el-button>
          <el-button
            type="danger"
            size="small"
            @click="handleDelete(scope.row)"
          >
            删除
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
import { onMounted, ref, reactive, computed } from 'vue';
import axios from 'axios';
import { ElMessage, ElMessageBox } from 'element-plus';

export default {
  name: 'AdminCommentsView',
  setup() {
    const loading = ref(false);
    const comments = ref([]);
    const totalComments = ref(0);
    const currentPage = ref(1);
    const pageSize = ref(20);
    const statusFilter = ref('');
    const searchKeyword = ref('');

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
      loading.value = true;
      try {
        const params = {
          page: currentPage.value,
          per_page: pageSize.value
        };

        if (statusFilter.value) {
          params.status = statusFilter.value;
        }

        if (searchKeyword.value) {
          params.search = searchKeyword.value;
        }

        const response = await axios.get('/api/admin/comments', { params });
        comments.value = response.data.comments;
        totalComments.value = response.data.total;
      } catch (error) {
        console.error('加载评论失败:', error);
        ElMessage.error('加载评论失败');
      } finally {
        loading.value = false;
      }
    };

    // 批准评论
    const handleApprove = async (comment) => {
      try {
        await axios.put(`/api/admin/comments/${comment.id}/approve`);
        comment.status = 'approved';
        ElMessage.success('评论已批准');
      } catch (error) {
        console.error('批准评论失败:', error);
        ElMessage.error('批准评论失败');
      }
    };

    // 驳回评论
    const handleReject = async (comment) => {
      try {
        await axios.put(`/api/admin/comments/${comment.id}/reject`);
        comment.status = 'pending';
        ElMessage.success('评论已驳回');
      } catch (error) {
        console.error('驳回评论失败:', error);
        ElMessage.error('驳回评论失败');
      }
    };

    // 删除评论
    const handleDelete = async (comment) => {
      ElMessageBox.confirm('确定要删除这条评论吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          await axios.delete(`/api/admin/comments/${comment.id}`);
          const index = comments.value.findIndex(item => item.id === comment.id);
          if (index !== -1) {
            comments.value.splice(index, 1);
            totalComments.value--;
          }
          ElMessage.success('评论已删除');
        } catch (error) {
          console.error('删除评论失败:', error);
          ElMessage.error('删除评论失败');
        }
      }).catch(() => {
        ElMessage.info('已取消删除');
      });
    };

    // 分页大小改变
    const handleSizeChange = (size) => {
      pageSize.value = size;
      currentPage.value = 1;
      loadComments();
    };

    // 当前页改变
    const handleCurrentChange = (current) => {
      currentPage.value = current;
      loadComments();
    };

    // 初始化
    onMounted(() => {
      loadComments();
    });

    // 计算属性，用于确保commentsData始终与comments同步
    const commentsData = computed(() => comments.value);
    
    return {
      loading,
      comments,
      commentsData,
      totalComments,
      currentPage,
      pageSize,
      statusFilter,
      searchKeyword,
      formatDate,
      getStatusTagType,
      getStatusText,
      handleApprove,
      handleReject,
      handleDelete,
      handleSizeChange,
      handleCurrentChange
    };
  }
};
</script>

<style scoped>
.admin-comments {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  font-size: 20px;
}

.comment-content {
  word-break: break-all;
  white-space: normal;
  line-height: 1.6;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>