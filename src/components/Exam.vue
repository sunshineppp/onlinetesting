<template>
  <div class="exam">

    <!-- slice(a,b)的作用是从已有的数组中返回选定的元素"a"表示开始，"b"表示结束。 -->
    <el-table :data="tableData.slice((currentPage - 1) * pageSize, currentPage * pageSize)" @row-click="handle" style="width: 100%;
      margin: auto;
      margin-top: 20px;
      box-shadow: 0px 5px 10px rgba(0, 0, 0, .12), 0px 5px 10px rgba(0, 0, 0, .04); " max-height="500">
      
      <!--
      <el-table-column fixed prop="id" label="试卷编号" width="100">
      </el-table-column>
      -->

      <el-table-column prop="name" label="试卷名称" width="120">
      </el-table-column>
      <el-table-column prop="created" label="创建日期" width="250">
      </el-table-column>
      <el-table-column prop="duration" label="考试时长" width="120">
      </el-table-column>
      <el-table-column prop="passline" label="合格分数" width="150">
      </el-table-column>
      <el-table-column fixed="right" label="操作" width="120">
        <template slot-scope="scope">
          <el-button @click="open" type="text" size="small">
            write
          </el-button>
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

  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'exam',
  data() {
    return {
      id: '',
      tableData: [],
      currentPage: 1, // 当前页码
      pageSize: 5 // 每页的数据条数
    }
  },
  methods: {
    //获取试卷信息
    getTabelInfo() {
      // const token = cookie.get('jwt')
      axios.get('/paper').then(res => {
        // console.log(res.data);
        this.tableData = res.data;//将后台传递的数组赋值给定义的空数组
        // console.log(this.tableData)//检查一下数组内是否有数据
      }).catch(res => {
        console.log("异常触发");
        console.log(res);//发生错误时执行的代码
      })
    },
    handle(row) {
      this.id = row.id;
      console.log(this.id);
    },
    open() {
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
    this.getTabelInfo(); //每次加载组件获取试卷信息
  },
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