<template>
  <el-card class="users-container">
    <template #header>
      <div class="users-header">
        <h1>用户管理</h1>
        <el-input
          v-model="searchQuery"
          placeholder="搜索用户名或邮箱..."
          prefix-icon="Search"
          style="width: 300px;"
          @input="handleSearch"
        />
      </div>
    </template>
    
    <!-- 用户表格 -->
    <el-table
      :data="filteredUsers"
      style="width: 100%"
      stripe
      border
      :loading="loading"
      empty-text="暂无用户数据"
    >
      <el-table-column prop="id" label="ID" width="80" type="index"></el-table-column>
      <el-table-column prop="username" label="用户名" width="180"></el-table-column>
      <el-table-column prop="email" label="邮箱" width="240"></el-table-column>
      <el-table-column prop="is_admin" label="角色" width="120">
        <template #default="scope">
          <el-tag :type="scope.row.is_admin ? 'primary' : 'default'">
            {{ scope.row.is_admin ? '管理员' : '普通用户' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template #default="scope">
          {{ formatDate(scope.row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="100">
        <template #default="scope">
          <el-tag :type="scope.row.status === 'active' ? 'success' : 'danger'">
            {{ scope.row.status === 'active' ? '活跃' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180" fixed="right">
        <template #default="scope">
          <el-button 
            type="primary" 
            size="small" 
            @click="openEditModal(scope.row)"
            :disabled="scope.row.id === currentUserId"
          >
            <el-icon><Edit /></el-icon>
            编辑
          </el-button>
          <el-button 
            type="danger" 
            size="small" 
            @click="confirmDelete(scope.row)"
            :disabled="scope.row.id === currentUserId"
          >
            <el-icon><Delete /></el-icon>
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <!-- 编辑用户模态框 -->
    <el-dialog
      v-model="showEditModal"
      title="编辑用户"
      width="500px"
      :before-close="closeEditModal"
    >
      <el-form ref="userForm" :model="editForm" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="editForm.username" disabled />
        </el-form-item>
        <el-form-item 
          label="邮箱" 
          prop="email" 
          :rules="[{ required: true, message: '请输入邮箱', trigger: 'blur' }, { type: 'email', message: '请输入有效的邮箱地址', trigger: ['blur', 'change'] }]"
        >
          <el-input v-model="editForm.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="角色" prop="is_admin" :rules="[{ required: true, message: '请选择角色', trigger: 'change' }]">
          <el-select v-model="editForm.is_admin" placeholder="请选择角色">
            <el-option label="普通用户" :value="false"></el-option>
            <el-option label="管理员" :value="true"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status" :rules="[{ required: true, message: '请选择状态', trigger: 'change' }]">
          <el-select v-model="editForm.status" placeholder="请选择状态">
            <el-option label="活跃" value="active"></el-option>
            <el-option label="禁用" value="disabled"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="closeEditModal">取消</el-button>
          <el-button type="primary" @click="handleUpdateUser" :loading="updating">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </el-card>
</template>

<script>
import { useAdminStore } from '../stores/admin.js';
import { useAuthStore } from '../stores/auth.js';
import { onMounted, ref, computed } from 'vue';
import { Search, Edit, Delete } from '@element-plus/icons-vue';
import { ElMessage, ElMessageBox } from 'element-plus';

export default {
  name: 'AdminUsersView',
  components: {
    Search,
    Edit,
    Delete
  },
  setup() {
    const adminStore = useAdminStore();
    const authStore = useAuthStore();
    
    const searchQuery = ref('');
    const showEditModal = ref(false);
    const editingUser = ref(null);
    const editForm = ref({});
    const updating = ref(false);
    
    // 加载用户列表
    onMounted(() => {
      loadUsers();
    });
    
    const loadUsers = async () => {
      try {
        await adminStore.getUsers();
      } catch (error) {
        console.error('Failed to load users:', error);
        ElMessage.error('加载用户列表失败');
      }
    };
    
    // 搜索用户
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
    
    // 打开编辑模态框
    const openEditModal = (user) => {
      editingUser.value = { ...user };
      editForm.value = {
        id: user.id,
        username: user.username,
        email: user.email,
        is_admin: user.is_admin,
        status: user.status || 'active'
      };
      showEditModal.value = true;
    };
    
    // 关闭编辑模态框
    const closeEditModal = () => {
      showEditModal.value = false;
      editingUser.value = null;
      editForm.value = {};
      updating.value = false;
    };
    
    // 更新用户
    const handleUpdateUser = async () => {
      try {
        updating.value = true;
        await adminStore.updateUser(editForm.value.id, editForm.value);
        await loadUsers();
        ElMessage.success('用户信息已更新');
        closeEditModal();
      } catch (error) {
        console.error('Failed to update user:', error);
        ElMessage.error('更新用户信息失败');
      } finally {
        updating.value = false;
      }
    };
    
    // 确认删除用户
    const confirmDelete = async (user) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除用户 ${user.username} 吗？此操作不可撤销。`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        );
        await handleDeleteUser(user.id);
      } catch (error) {
        // 用户取消删除操作
        if (error !== 'cancel') {
          console.error('Delete confirmation failed:', error);
        }
      }
    };
    
    // 删除用户
    const handleDeleteUser = async (userId) => {
      try {
        await adminStore.deleteUser(userId);
        await loadUsers();
        ElMessage.success('用户已删除');
      } catch (error) {
        console.error('Failed to delete user:', error);
        ElMessage.error('删除用户失败');
      }
    };
    
    // 过滤用户列表
    const filteredUsers = computed(() => {
      if (!searchQuery.value) return adminStore.users;
      
      const query = searchQuery.value.toLowerCase();
      return adminStore.users.filter(user => 
        user.username.toLowerCase().includes(query) ||
        user.email.toLowerCase().includes(query)
      );
    });
    
    // 获取当前登录用户ID
    const currentUserId = computed(() => {
      return authStore.user?.id;
    });
    
    return {
      searchQuery,
      showEditModal,
      editingUser,
      editForm,
      updating,
      users: adminStore.users,
      loading: adminStore.loading,
      handleSearch,
      formatDate,
      openEditModal,
      closeEditModal,
      handleUpdateUser,
      confirmDelete,
      filteredUsers,
      currentUserId
    };
  }
};
</script>

<style scoped>
.users-container {
  margin: 20px;
}

.users-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.users-header h1 {
  margin: 0;
  color: #333;
  font-size: 20px;
  font-weight: 600;
}

.el-table .el-button + .el-button {
  margin-left: 10px;
}

.el-table .el-button:disabled {
  opacity: 0.5;
}
</style>