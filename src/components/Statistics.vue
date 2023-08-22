<template>
    <div class="statistics">
        <el-dialog title="View" :visible.sync="dialogVisible" @open="open()" append-to-body>
            <div ref="EChart" style="width: 550px; height: 300px;"></div>
        </el-dialog>

        <el-table :data="tableData.slice((currentPage - 1) * pageSize, currentPage * pageSize)" style="
                width: 100%;
                margin: auto;
                margin-top: 20px;
                max-height: 500px;
            ">
            <el-table-column fixed prop="id" label="试卷编号" width="100">
            </el-table-column>
            <el-table-column prop="name" label="考试名称" width="150">
            </el-table-column>
            <el-table-column prop="created" label="创建日期" width="150">
            </el-table-column>
            <el-table-column prop="duration" label="考试时长" width="150">
            </el-table-column>
            <el-table-column prop="passline" label="合格分数" width="100">
            </el-table-column>
            <el-table-column prop="fullPoints" label="总分" width="100">
            </el-table-column>
            <el-table-column prop="notProcessed" label="未批改人数" width="100">
            </el-table-column>
            <el-table-column prop="passNumber" label="合格人数" width="100">
            </el-table-column>
            <el-table-column prop="totalNumber" label="考试总人数" width="100">
            </el-table-column>
            <el-table-column fixed="right" prop="" label="操作" width="100">
                <template slot-scope="scope">
                    <el-button type="primary" size="medium"
                        @click="click(scope.row.notProcessed, scope.row.passNumber, scope.row.totalNumber)">
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

export default {
    name: 'statistics',
    data() {
        return {
            dialogVisible: false,
            notProcessed: '', //未批改人数
            passNumber: '', //合格人数
            totalNumber: '', //考试总人数
            tableData: [],
            currentPage: 1, // 当前页码
            pageSize: 5, // 每页的数据数条
            option1:
            {

            }
        }
    },
    methods: {
        click(notProcessed, passNumber, totalNumber) {
            this.notProcessed = notProcessed;
            this.passNumber = passNumber;
            this.totalNumber = totalNumber;
            this.dialogVisible = true;
        },
        open() {
            setTimeout(() => {
                this.drawLine(this.notProcessed, this.passNumber, this.totalNumber);
            }, 0);
        },
        drawLine(notProcessed, passNumber, totalNumber) {
            let EChart = this.$echarts.init(this.$refs.EChart);
            let option2 =
            {
                legend: {
                    data: ["未批改人数", "合格人数", "不合格人数"],
                    right: "10%",
                    top: "30%",
                    orient: "vertical"
                },
                title: {
                    text: "考试情况",
                    top: "0%",
                    left: "center",
                },
                series: [
                    {
                        type: 'pie',
                        stillShowZeroSum: false,
                        label: {
                            show: false
                        },
                        data: [
                            {
                                value: notProcessed,
                                name: '未批改人数'
                            },
                            {
                                value: passNumber,
                                name: '合格人数'
                            },
                            {
                                value: (totalNumber - notProcessed - passNumber),
                                name: '不合格人数'
                            }
                        ]
                    }
                ]
            };
            EChart.setOption(option2);
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
        axios.get('/statistics/exam', { headers: { 'Authorization': token } }).then(res => {
            console.log(res.data);
            this.tableData = res.data;
        }).catch(res => {
            console.log("触发异常");
            console.log(res)
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