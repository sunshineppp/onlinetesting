<template>
  <div class="permissions">

    <el-container>

      <el-header style="background-color: #fff;">
        <!-- dialogForm -->
        <div style="margin-right: 10px; text-align: right;">
          <el-button type="primary" round @click="resetForm2()">添加</el-button>
        </div>
      </el-header>

      <!-- 表单 -->
      <el-dialog :title=type :visible.sync="dialogFormVisible" append-to-body>
        <el-form :model="form" :rules="rules" ref="form" label-position="right">
          <el-form-item label="用户名" prop="account" :label-width="formLabelWidth">
            <el-input v-model="form.account" autocomplete="off" placeholder="account"
              :disabled="type != 'Add'"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password" v-show="type != 'View'" :label-width="formLabelWidth">
            <el-input v-model="form.password" autocomplete="off" placeholder="password"
              :disabled="type == 'View'"></el-input>
          </el-form-item>
          <el-form-item label="邮箱" prop="email" :label-width="formLabelWidth">
            <el-input v-model="form.email" autocomplete="off" placeholder="email" :disabled="type == 'View'"></el-input>
          </el-form-item>
          <el-form-item label="权限" prop="permission_name" v-show="type == 'View'" :label-width="formLabelWidth">
            <el-input v-model="form.permission_name" autocomplete="off" placeholder="email"
              :disabled="type == 'View'"></el-input>
          </el-form-item>
          <el-form-item label="权限等级" prop="permission_id" v-show="type != 'View'" :label-width="formLabelWidth">
            <el-select v-model="form.permission_id" placeholder="请选择权限" :disabled="type == 'View'">
              <el-option label="超级管理员" value=3></el-option>
              <el-option label="教师" value=2></el-option>
              <el-option label="学生" value=1></el-option>
            </el-select>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="resetForm('form')">取 消</el-button>
          <el-button type="primary" @click="submitForm('form')" v-show="type != 'View'">确 定</el-button>
        </div>
      </el-dialog>

      <!-- Table -->
      <!-- slice(a,b)的作用是从已有的数组中返回选定的元素"a"表示开始，"b"表示结束。 -->
      <el-table :data="tableData.slice((currentPage - 1) * pageSize, currentPage * pageSize)" style="
          width: 100%;
          margin: auto;
          margin-top: 10px;" max-height="500" @row-click="handle
            ">

        <!--
      <el-table-column fixed prop="id" label="序列" width="50">
      </el-table-column>
      -->

        <el-table-column fixed prop="account" label="用户名" width="150">
        </el-table-column>
        <el-table-column prop="permission_id" label="权限等级" width="150">
        </el-table-column>
        <el-table-column prop="email" label="邮箱" width="150">
        </el-table-column>
        <el-table-column fixed="right" label="操作" width="300">
          <template slot-scope="scope">
            <el-button-group>
              <el-button size="medium" plain icon="el-icon-search" @click="View">查看</el-button>
              <el-button size="medium" plain icon="el-icon-edit" @click="Revise">修改</el-button>
              <el-button size="medium" type="danger" plain icon="el-icon-delete" @click="Delete">删除</el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>

      <el-footer>
        <!-- 分页器 -->
        <div class="pagination" style="margin-top:">
          <el-pagination align='center' @size-change="handleSizeChange" @current-change="handleCurrentChange"
            :current-page="currentPage" :page-sizes="[1, 5, 10, 20]" :page-size="pageSize"
            layout="total, sizes, prev, pager, next, jumper" :total="tableData.length">
          </el-pagination>
        </div>
      </el-footer>

    </el-container>

  </div>
</template>
  
<script>
import axios from 'axios'
import cookie from 'js-cookie'

export default {
  name: 'permissions',
  data() {
    return {
      id: '',
      type: '',
      dialogFormVisible: false, //对话框
      visible: false, //弹出框

      formLabelWidth: '120px',
      tableData: [],
      currentPage: 1, // 当前页码
      pageSize: 5, // 每页的数据数条

      form: {
        account: '',
        password: '',
        email: '',
        permission_id: '',
        permission_name: '',
      },

      //表单规则
      rules: {
        account: [
          { required: true, message: '请输入用户名称', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 8, max: 16, message: '长度在 8 到 16 个字符', trigger: 'blur' }
        ],
        email: [
          { required: true, message: '请输入邮箱', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }
        ],
        permission_id: [
          { required: true, message: '请选择权限等级', trigger: 'change' }
        ]
      },
    }
  },
  methods: {

    //判别权限名称
    permissionsName(id) {
      switch (id) {
        case (0): return "游客"; break;
        case (1): return "学生"; break;
        case (2): return "教师"; break;
        case (3): return "超级管理员"; break;
      }
    },

    //获取用户信息
    getTabelInfo() {
      const token = cookie.get('jwt')
      axios.get('/api/users/', { headers: { 'Authorization': token } }).then(res => {
        // console.log(res.data.items);
        this.tableData = res.data.users;//将后台传递的数组赋值给定义的空数组
        for (let i in this.tableData) {
          this.tableData[i].permission_id = this.permissionsName(this.tableData[i].permission_id);
        }
        console.log("getTabelInfo");
        // console.log(this.tableData)//检查一下数组内是否有数据
      }).catch(res => {
        console.log("异常触发");
        console.log(res);//发生错误时执行的代码
      })
    },

    //添加用户
    addUser() {
      const token = cookie.get('jwt')
      axios.post('/api/users/adminCreate', this.form, { headers: { 'Authorization': token } }).then(res => {
        alert('添加成功!');
        this.getTabelInfo();
        this.dialogFormVisible = false;
      }).catch(reason => {
        console.log("异常触发");
        console.log(reason);
      })
    },

    //修改用户
    reviseUser(id) {
      const token = cookie.get('jwt')
      axios.post('/api/users/' + id, this.form, { headers: { 'Authorization': token } }).then(res => {
        alert('修改成功!');
        this.getTabelInfo();
        this.dialogFormVisible = false;
      }).catch(reason => {
        console.log("异常触发");
        console.log(reason);
      })
    },

    //删除用户
    deleteUser(id) {
      const token = cookie.get('jwt')
      console.log(this.id);
      axios.delete('/api/users/' + id, { headers: { 'Authorization': token } }).then(res => {
        alert('删除成功!');
        this.currentPage = 1;
        this.getTabelInfo();
      }).catch(res => {
        console.log("异常触发");
        console.log(res);//发生错误时执行的代码
      })
    },

    //表单输入限制
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          console.log(this.form); //输出当前表单信息
          if (this.type == "Add") {
            console.log("Add");
            this.addUser();
          }
          else if (this.type == "Revise") {
            console.log("Revise");
            console.log(this.id);
            this.reviseUser(this.id);
          }
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },

    //重置表单
    resetForm(formName) {
      this.dialogFormVisible = false;
      this.$refs[formName].resetFields();
    },

    //点击添加按钮清空form
    resetForm2() {
      this.form.account = this.form.password = this.form.email = this.form.permission_id = this.form.permission_name = '';
      this.dialogFormVisible = true;
      this.type = 'Add';
    },

    //表格操作事件
    handle(row) {
      this.id = row.id;
      this.form.account = row.account;
      this.form.email = row.email;
      this.form.permission_name = row.permission_id;
    },

    View() {
      this.type = "View";
      this.dialogFormVisible = true;
    },

    Revise() {
      this.type = "Revise";
      this.dialogFormVisible = true;
    },

    Delete() {
      this.$confirm('此操作将永久删除,是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.deleteUser(this.id);
      }).catch(() => {
        alert('已取消删除!');
      });
    },

    //每页条数改变时触发 选择一页显示多少行
    handleSizeChange(val) {
      console.log(`每页 ${val} 条`);
      this.currentPage = 1;
      this.pageSize = val;
    },
    //当前页改变时触发 跳转其他页
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`);
      this.currentPage = val;
    }
  },
  mounted() {
    this.getTabelInfo(); //每次加载组件获取信息
  },
}
</script>
    
  <!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.permissions {
  height: 100%;
  opacity: 0.9;
}

.pagination {
  position: fixed;
  bottom: 0;
  height: 40px;
  width: 100%;
  text-align: center;
}

* {
  border-radius: 4px;
  /* 设置组件内所有标签为圆角矩阵 */
}
</style>