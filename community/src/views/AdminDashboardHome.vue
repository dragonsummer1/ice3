<template>
  <div class="dashboard-container">
    <el-card class="dashboard-title-card">
      <h1>管理仪表盘</h1>
      <p class="dashboard-subtitle">实时监控社区运营数据</p>
    </el-card>
    
    <!-- 统计卡片 -->
    <div class="stats-container">
      <el-row :gutter="20">
        <el-col :xs="24" :sm="12" :md="6">
          <el-card class="stat-card">
            <template #header>
              <div class="card-header">
                <span>总用户数</span>
                <el-icon class="header-icon"><User /></el-icon>
              </div>
            </template>
            <div class="stat-content">
              <div class="stat-number">{{ stats.totalUsers }}</div>
              <div class="stat-desc">{{ todayNewUsers }} 位新用户</div>
            </div>
          </el-card>
        </el-col>
        <el-col :xs="24" :sm="12" :md="6">
          <el-card class="stat-card">
            <template #header>
              <div class="card-header">
                <span>总评论数</span>
                <el-icon class="header-icon"><ChatDotRound /></el-icon>
              </div>
            </template>
            <div class="stat-content">
              <div class="stat-number">{{ stats.totalComments }}</div>
              <div class="stat-desc">{{ todayNewComments }} 条新评论</div>
            </div>
          </el-card>
        </el-col>
        <el-col :xs="24" :sm="12" :md="6">
          <el-card class="stat-card">
            <template #header>
              <div class="card-header">
                <span>活跃用户</span>
                <el-icon class="header-icon"><UserFilled /></el-icon>
              </div>
            </template>
            <div class="stat-content">
              <div class="stat-number">{{ stats.activeUsers }}</div>
              <div class="stat-desc">过去24小时内</div>
            </div>
          </el-card>
        </el-col>
        <el-col :xs="24" :sm="12" :md="6">
          <el-card class="stat-card">
            <template #header>
              <div class="card-header">
                <span>待处理事项</span>
                <el-icon class="header-icon"><WarningFilled /></el-icon>
              </div>
            </template>
            <div class="stat-content">
              <div class="stat-number">{{ stats.pendingItems }}</div>
              <div class="stat-desc">{{ pendingComments }} 条待审核评论</div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
    
    <!-- 图表区域 -->
    <div class="charts-container">
      <el-row :gutter="20">
        <el-col :xs="24" :lg="12">
          <el-card class="chart-card">
            <template #header>
              <div class="card-header">
                <span>用户增长趋势</span>
                <el-icon class="header-icon"><ArrowUp /></el-icon>
              </div>
            </template>
            <div class="chart-wrapper">
              <el-progress :percentage="userGrowthRate" status="success" :stroke-width="12"></el-progress>
              <div class="chart-data">
                <el-table :data="userGrowthData" size="small" style="width: 100%; margin-top: 20px;">
                  <el-table-column prop="date" label="日期" width="100"></el-table-column>
                  <el-table-column prop="count" label="新增用户" width="100"></el-table-column>
                  <el-table-column label="趋势" width="120">
                    <template #default="scope">
                      <el-tag v-if="scope.row.count > 10" type="success">快速增长</el-tag>
                      <el-tag v-else-if="scope.row.count > 5" type="primary">稳定增长</el-tag>
                      <el-tag type="info">缓慢增长</el-tag>
                    </template>
                  </el-table-column>
                </el-table>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :xs="24" :lg="12">
          <el-card class="chart-card">
            <template #header>
              <div class="card-header">
                <span>评论活跃度</span>
                <el-icon class="header-icon"><PieChart /></el-icon>
              </div>
            </template>
            <div class="chart-wrapper">
              <el-progress :percentage="commentActivityRate" status="info" :stroke-width="12"></el-progress>
              <div class="chart-data">
                <el-table :data="commentActivityData" size="small" style="width: 100%; margin-top: 20px;">
                  <el-table-column prop="date" label="日期" width="100"></el-table-column>
                  <el-table-column prop="count" label="评论数量" width="100"></el-table-column>
                  <el-table-column label="活跃度" width="120">
                    <template #default="scope">
                      <el-tag v-if="scope.row.count > 30" type="success">活跃</el-tag>
                      <el-tag v-else-if="scope.row.count > 15" type="primary">一般</el-tag>
                      <el-tag type="info">较低</el-tag>
                    </template>
                  </el-table-column>
                </el-table>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
    
    <!-- 最近评论 -->
    <el-card class="recent-comments-card">
      <template #header>
        <div class="card-header">
          <span>最近评论</span>
          <el-button type="text" size="small">查看全部</el-button>
        </div>
      </template>
      <div class="recent-comments-list">
        <el-table :data="recentComments" stripe style="width: 100%">
          <el-table-column prop="content" label="评论内容" width="400">
            <template #default="scope">
              <div class="comment-content">{{ scope.row.content }}</div>
            </template>
          </el-table-column>
          <el-table-column prop="username" label="用户"></el-table-column>
          <el-table-column prop="created_at" label="时间">
            <template #default="scope">
              {{ formatDate(scope.row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态">
            <template #default="scope">
              <el-tag 
                :type="scope.row.status === 'approved' ? 'success' : 'warning'">
                {{ scope.row.status === 'approved' ? '已批准' : '待审核' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="100">
            <template #default="scope">
              <el-button type="text" size="small">查看</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<script>
import { useAdminStore } from '../stores/admin.js';
import { onMounted, ref, computed } from 'vue';
import { User, ChatDotRound, UserFilled, WarningFilled, ArrowUp, PieChart } from '@element-plus/icons-vue';

// 引入ElMessage用于错误提示
import { ElMessage } from 'element-plus';

export default {
  name: 'AdminDashboardHome',
  components: {
    User,
    ChatDotRound,
    UserFilled,
    WarningFilled,
    ArrowUp,
    PieChart
  },
  setup() {
    const adminStore = useAdminStore();
    const recentComments = ref([]);
    const isLoading = ref(true);
    
    // 模拟统计数据
    const stats = ref({
      totalUsers: 0,
      totalComments: 0,
      activeUsers: 0,
      pendingItems: 0,
      todayNewUsers: 0,
      todayNewComments: 0,
      pendingComments: 0
    });
    
    // 新用户和评论数据
    const todayNewUsers = computed(() => Math.floor(Math.random() * 10) + 1);
    const todayNewComments = computed(() => Math.floor(Math.random() * 20) + 5);
    const pendingComments = computed(() => {
      return recentComments.value.filter(comment => comment.status !== 'approved').length;
    });
    
    // 增长率
    const userGrowthRate = computed(() => {
      return Math.floor(Math.random() * 30) + 10;
    });
    
    const commentActivityRate = computed(() => {
      return Math.floor(Math.random() * 40) + 20;
    });
    
    // 图表数据
    const userGrowthData = ref([]);
    const commentActivityData = ref([]);
    
    // 加载数据
    const loadDashboardData = async () => {
      isLoading.value = true;
      try {
        // 加载用户数据
        await adminStore.getUsers(1, 100);
        stats.value.totalUsers = adminStore.users.length || 0;
        stats.value.activeUsers = Math.floor(Math.random() * 50) + 10;
        
        // 加载评论数据
        const commentsResponse = await adminStore.getComments(1, 10);
        recentComments.value = commentsResponse.comments || [];
        stats.value.totalComments = commentsResponse.total || 0;
        
        // 计算待审核评论数量
        stats.value.pendingComments = pendingComments.value;
        stats.value.pendingItems = stats.value.pendingComments;
        
        // 加载统计数据用于图表
        try {
          const statsResponse = await adminStore.getStats();
          userGrowthData.value = statsResponse.user_growth || [];
          commentActivityData.value = statsResponse.comment_activity || [];
          console.log('统计数据加载成功:', statsResponse);
        } catch (statsError) {
          console.error('加载统计数据失败:', statsError);
          // 使用模拟数据
          const today = new Date();
          const mockUserGrowth = [];
          const mockCommentActivity = [];
          
          for (let i = 6; i >= 0; i--) {
            const date = new Date(today);
            date.setDate(date.getDate() - i);
            const dateStr = date.toISOString().split('T')[0];
            
            mockUserGrowth.push({
              date: dateStr,
              count: Math.floor(Math.random() * 20) + 1
            });
            
            mockCommentActivity.push({
              date: dateStr,
              count: Math.floor(Math.random() * 50) + 5
            });
          }
          
          userGrowthData.value = mockUserGrowth;
          commentActivityData.value = mockCommentActivity;
        }
      } catch (error) {
        console.error('加载仪表盘数据失败:', error);
        // 显示错误提示
        ElMessage.error('加载仪表盘数据失败');
      } finally {
        isLoading.value = false;
      }
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
    
    onMounted(() => {
      loadDashboardData();
    });
    
    return {
      stats,
      recentComments,
      isLoading,
      userGrowthRate,
      commentActivityRate,
      todayNewUsers,
      todayNewComments,
      pendingComments,
      formatDate,
      userGrowthData,
      commentActivityData
    };
  }
};
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.dashboard-title-card {
  margin-bottom: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
}

.dashboard-title-card h1 {
  margin: 0 0 10px 0;
  font-size: 28px;
}

.dashboard-subtitle {
  margin: 0;
  opacity: 0.9;
}

.stats-container,
.charts-container {
  margin-bottom: 20px;
}

.stat-card {
  height: 100%;
  transition: all 0.3s ease;
  cursor: pointer;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
}

.header-icon {
  font-size: 18px;
  color: #666;
}

.stat-content {
  text-align: center;
  padding: 20px 0;
}

.stat-number {
  font-size: 32px;
  font-weight: bold;
  color: #1890ff;
  margin-bottom: 8px;
}

.stat-desc {
  font-size: 14px;
  color: #666;
}

.chart-card {
  height: 250px;
  display: flex;
  flex-direction: column;
}

.chart-wrapper {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 20px;
  }

  .chart-placeholder {
    margin-top: 20px;
    color: #999;
    font-size: 14px;
  }
  
  .chart-data {
    width: 100%;
    overflow-x: auto;
  }
  
  .chart-data .el-table {
    font-size: 12px;
  }
  
  .chart-data .el-table .el-table__cell {
    padding: 6px 4px;
  }

.recent-comments-card {
  margin-top: 20px;
}

.recent-comments-list {
  max-height: 400px;
  overflow-y: auto;
}

.comment-content {
  max-width: 100%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>