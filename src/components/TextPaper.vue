<template>
  <div class="textPaper">
    <el-header style="background-color: #fff;">
      <!-- dialogForm -->
      <div style="margin-right: 10px; text-align: right;">
        <el-button type="primary" round @click="addPaper()">添加</el-button>
      </div>
    </el-header>
    <!-- slice(a,b)的作用是从已有的数组中返回选定的元素"a"表示开始，"b"表示结束。 -->
    <el-table :data="tableData.slice((currentPage - 1) * pageSize, currentPage * pageSize)" @row-click="handle" style="width: 100%;
      margin: auto;
      margin-top: 20px;
      box-shadow: 0px 5px 10px rgba(0, 0, 0, .12), 0px 5px 10px rgba(0, 0, 0, .04); " max-height="500">
      <el-table-column fixed prop="id" label="试卷编号" width="100">
      </el-table-column>
      <el-table-column prop="name" label="试卷名称" width="120">
      </el-table-column>
      <el-table-column prop="created" label="创建日期" width="250">
      </el-table-column>
      <el-table-column prop="duration" label="考试时长" width="120">
      </el-table-column>
      <el-table-column prop="passline" label="及格分数线" width="150">
      </el-table-column>
      <el-table-column fixed="right" label="操作" width="250">
        <template slot-scope="scope">
          <el-button-group>
            <!-- <el-button size="medium" plain icon="el-icon-search" @click="checkPaper(scope.row.id)">查看</el-button> -->
            <el-button size="medium" plain type="primary" icon="el-icon-edit"
              @click="modifyPaper(scope.row.id)">修改</el-button>
            <el-button size="medium" type="danger" plain icon="el-icon-delete"
              @click="deletePaper(scope.row.id)">删除</el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页器 -->
    <div class="pagination" style="margin-top:">
      <el-pagination align='center' @size-change="handleSizeChange" @current-change="handleCurrentChange"
        :current-page="currentPage" :page-sizes="[1, 5, 10, 20]" :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper" :total="tableData.length">
      </el-pagination>
    </div>

    <router-view />

  </div>
</template>
  
<script>
import axios from 'axios'
import cookie from 'js-cookie'

export default {
  name: 'textPaper',
  data() {
    return {
      tableData: [],
      currentPage: 1, // 当前页码
      pageSize: 5 // 每页的数据条数
    }
  },
  methods: {

    addPaper() {
      this.$router.push({ name: 'createPaper' }).catch(() => { })
    },

    // checkPaper() {

    // },

    deletePaper(id) {
      let token = cookie.get('jwt')
      axios.delete('/paper/delete/' + id, { headers: { 'Authorization': token } })
        .then(() => {
          this.$notify({
            type: 'success',
            title: '删除成功'
          })
          return axios.get('/paper', { headers: { 'Authorization': token } })
        })
        .then((res) => {
          this.tableData = res.data
        })
        .catch(err => {
          console.log(err)
        })
    },

    modifyPaper(id) {
      this.$router.push({name: 'updatePaper', params: {'paper_id': id}})
    },

    open() {
    },

    handle(row) {

    },

    //每页条数改变时触发 选择一页显示多少行
    handleSizeChange(val) {
      console.log(`每页 ${val} 条`); this.currentPage = 1;
      this.pageSize = val;
    },

    //当前页改变时触发 跳转其他页
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`);
      this.currentPage = val;
    }
  },
  created() {
    const token = cookie.get('jwt')
    axios.get('/paper', { headers: { 'Authorization': token } })
      .then((response) => {
        this.tableData = response.data
      }).catch((error) => {
        console.log(error)
      })
  }
}
</script>
  
  <!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.exam {
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
  