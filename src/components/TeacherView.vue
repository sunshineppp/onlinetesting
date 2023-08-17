<template>
    <div style="width: 70%; margin: auto; background-color: #fff;">
        <el-form :model="CorrectPaper" label-position="right" style="text-align: center;">
            <template v-for="(item, index) in CorrectPaper.questions">

                <!-- 题干 -->
                <p>{{ item.content }} ({{ item.point }}分)</p>

                <!-- 选择、判断题 -->
                <div v-show="item.type == 'singleChoice' || item.type == 'trueOrFalse'">
                    <el-radio-group v-model="item.user_exams[0].answer">
                        <el-radio v-for="answer in item.answers" :label="answer.id.toString()" :disabled="true">
                            {{ answer.content }}
                        </el-radio>
                    </el-radio-group>

                    <div>
                        <el-form-item label="题目得分:">
                            <el-input-number size="medium" v-model="item.user_exams[0].score" :min="0"
                                :max="item.point" :disabled="item.type != 'shortAnswer'">
                            </el-input-number>
                        </el-form-item>
                    </div>
                </div>

                <!-- 主观题 -->
                <div v-show="item.type == 'shortAnswer'">
                    <el-input v-model="item.user_exams[0].answer" :disabled="true"></el-input>

                    <div>
                        <el-form-item label="题目得分:">
                            <el-input-number size="medium" v-model="item.user_exams[0].score" :min="0"
                                :max="item.point" @change="qs(index)">
                            </el-input-number>
                        </el-form-item>
                    </div>
                </div>

                <!-- 答案解析 -->
                <p>解析：{{ item.analysis }}</p>

                <!-- 分割线 -->
                <el-divider></el-divider>
            </template>
            <el-form-item>
                <el-button type="primary" @click="">批改完成</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
import cookie from 'js-cookie'
import axios from 'axios'

export default {
    data() {
        return {
            CorrectPaper: {
                questions: []
            },
            form: {
                questions: []
            },
        }
    },
    methods: {
        // submitForm() {
        //     console.log(this.form);
        //     this.$confirm('确认交卷?', '提示', {
        //         confirmButtonText: '是',
        //         cancelButtonText: '否',
        //         type: 'warning'
        //     }).then(() => {
        //         const token = cookie.get('jwt')
        //         axios.post('/wrong/myExam', this.form, { headers: { 'Authorization': token } })
        //             .then(() => {
        //                 this.$router.push({ name: 'exam' })
        //             })
        //             .catch(res => {
        //                 console.log("异常触发");
        //                 console.log(res); //发生错误时执行的代码
        //             })
        //     }).catch(() => {
        //         alert('已取消交卷!');
        //     })
        // }
        qs(index){
            console.log(this.CorrectPaper.questions[index].user_exams[0].score);
        }
    },
    created() {
        let user_id = this.$route.params.user_id;
        let testpaper_id_ = this.$route.params.testpaper_id_;
        if (user_id !== undefined && testpaper_id_ !== undefined) {
            const token = cookie.get('jwt')
            axios.get('/wrong/correctPaper/' + user_id + '/' + testpaper_id_, { headers: { 'Authorization': token } }).then(res => {
                // console.log(res.data.questions);
                // console.log(res.data.questions[0].user_exams[0].score);
                this.CorrectPaper.questions = res.data.questions;
                console.log(this.CorrectPaper);

                // let j = 0;
                // for (let i = 0; i < this.CorrectPaper.questions.length; i++) {
                //     if (this.CorrectPaper[i].type == "shortAnswer") {
                //         this.form.questions[j] = {
                //             question_id: this.CorrectPaper.questions[i].id,
                //             question_score: ''
                //         }
                //         j++;
                //     }
                // }
                // console.log(this.form);
            }).catch(res => {
                console.log("异常触发");
                console.log(res);
            })
        }
        else {
            this.$router.push({ name: 'teacher' })
        }
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