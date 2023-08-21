<template>
    <div style="width: 100%; margin: auto; background-color: #fff;">
        <el-form :model="CorrectPaper" ref="CorrectPaper" label-position="left" style="text-align: center;">
            <div v-for="(item, index) in CorrectPaper.questions" :key="index"
                style="width: 450px; margin:auto; padding: 10px;">

                <!-- 题干 -->
                <p>{{ item.content }} ({{ item.point }}分)</p>

                <!-- <ul v-show="item.type == 'singleChoice'" style="padding-left: 20px;">
                    <li  v-for="answer in item.answers">
                    {{ answer.content }}
                    </li>
                </ul> -->

                <!-- 选择、判断题 -->
                <div v-show="item.type == 'singleChoice' || item.type == 'trueOrFalse'" style="
                        text-align: left;
                        padding-left: 50px;
                    ">
                    <el-radio-group v-model="item.user_exams[0].answer">
                        <div v-for="answer in item.answers" style="
                                /* margin: 50px,0px; */
                            ">
                            <el-radio :label="answer.id.toString()" :disabled="true">
                                {{ answer.content }}
                            </el-radio>
                        </div>
                    </el-radio-group>
                </div>

                <!-- 主观题 -->
                <div v-show="item.type == 'shortAnswer'">
                    <el-input v-model="item.user_exams[0].answer" style="width: 50%;" :disabled="true"></el-input>
                </div>

                <!-- 答案解析 -->
                <p>解析：{{ item.analysis }}</p>

                <div>
                    <!-- :prop="questions[index].user_exams[0].score" :rules="[ { required: true, message: '请输入题目得分', trigger: 'blur' }]" -->
                    <el-form-item label="题目得分:" :prop="`questions[${index}].user_exams[0].score`"
                        :rules="{ required: true, message: '请输入题目得分', trigger: 'blur' }">
                        <el-input-number size="medium" v-model="item.user_exams[0].score" :min="0" :max="item.point"
                            @change="qs(index)" :disabled=true>
                        </el-input-number>
                    </el-form-item>
                </div>

                <!-- 分割线 -->
                <el-divider></el-divider>
            </div>
            <el-form-item>
                <el-button type="primary" @click="submitForm('CorrectPaper')">返回</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
import cookie from 'js-cookie'
import axios from 'axios'
import router from '@/router';

export default {
    data() {
        return {
            CorrectPaper: {
                questions: []
            },
            form: {
                questions: []
            },
            // rules: {
            //     questions: [
            //         { required: true, message: '请输入题目得分', trigger: 'blur' }
            //     ]
            // }
        }
    },
    methods: {
        submitForm(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    let j = 0;
                    for (let i = 0; i < this.CorrectPaper.questions.length; i++) {
                        if (this.CorrectPaper.questions[i].type == "shortAnswer") {
                            this.form.questions[j] = {
                                question_id: this.CorrectPaper.questions[i].id,
                                question_score: this.CorrectPaper.questions[i].user_exams[0].score
                            }
                            j++;
                        }
                    }
                    console.log(this.form);

                    let user_id = this.$route.params.user_id;
                    let testpaper_id_ = this.$route.params.testpaper_id_;
                    const token = cookie.get('jwt')
                    axios.post('/wrong/correctPaper/' + user_id + '/' + testpaper_id_, this.form, { headers: { 'Authorization': token } }).then(res => {
                        alert('批改成功！');
                        router.push({ name: 'teacher' });
                    }).catch(res => {
                        console.log("异常触发");
                        console.log(res);
                    })
                } else {
                    console.log('error submit!!');
                    return false;
                }
            });
        },
        qs(index) {
            console.log(this.CorrectPaper.questions[index].user_exams[0].score);
        }
    },
    created() {
        let exam_id = this.$route.params.exam_id;
        if (exam_id !== undefined) {
            const token = cookie.get('jwt')
            axios.get('/wrong/myExamDetil/' + exam_id, { headers: { 'Authorization': token } }).then(res => {
                // console.log(res.data.questions);
                // console.log(res.data.questions[0].user_exams[0].score);
                this.CorrectPaper.questions = res.data.questions;
                console.log(this.CorrectPaper);
            }).catch(res => {
                console.log("异常触发");
                console.log(res);
            })
        }
        else {
            console.log("id为空");
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