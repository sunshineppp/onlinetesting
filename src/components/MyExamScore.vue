<template>
    <div class="myExamScore">
        <el-table :data="tableData.slice((currentPage - 1) * pageSize, currentPage * pageSize)" style="
                width: 100%;
                margin: auto;
                margin-top: 20px;
                max-height: 500px;
            ">
            <el-table-column fixed prop="exam_name" label="考试名称" width="150">
            </el-table-column>
            <el-table-column prop="exam_total_score" label="总分" width="100">
            </el-table-column>
            <el-table-column prop="exam_pass_score" label="合格分数" width="100">
            </el-table-column>
            <el-table-column prop="score" label="我的分数" width="100">
            </el-table-column>
            <el-table-column prop="pass_or_not" label="是否合格" width="100">
            </el-table-column>
            <el-table-column prop="exam_time" label="考试时间" width="200">
            </el-table-column>
            <el-table-column fixed="right" prop="" label="操作" width="100">
                <template slot-scope="scope">
                    <el-button type="primary" size="medium" @click="View(scope.row.exam_id)">
                        查看
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
import cookie from 'js-cookie'
import axios from 'axios'
import router from '@/router'

export default {
    name: 'myExamScore',
    data() {
        return {
            tableData: [],
            currentPage: 1, // 当前页码
            pageSize: 5, // 每页的数据数条
        }
    },
    methods: {
        View(id) {
            router.push({ name: 'myExamScoreView', params: { exam_id: id } });
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
    created() {
        const token = cookie.get('jwt')
        axios.get('/wrong/myExamScore', { headers: { 'Authorization': token } }).then(res => {
            console.log(res.data);
            this.tableData = res.data;
            for (let i = 0; i < this.tableData.length; i++) {
                if (this.tableData[i].score == -1) {
                    this.tableData[i].score = '无';
                }
            }
            for (let exam of this.tableData) {
                let date = new Date(Date.parse(exam.exam_time))
                exam.exam_time = `${date.getUTCFullYear()} 年 ${date.getUTCMonth() + 1} 月 ${date.getUTCDate()} 日`
            }
        }).catch(res => {
            console.log("触发异常");
            console.log(res);
        })
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.teacher {
    opacity: 0.9;
}

/* 分页样式 */
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