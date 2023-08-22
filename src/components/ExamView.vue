<template>
    <el-row :gutter="20">
        <el-col :span="4">
            <el-tag type="danger">
                <countdown :time="duration" @progress="handleProgress">
                    <template slot-scope="props">
                        剩余时间: {{ props.hours }} 小时,
                        {{ props.minutes }}分钟,
                        {{ props.seconds }} 秒.
                    </template>
                </countdown>
            </el-tag>
        </el-col>
        <el-col :span="16">
            <el-form :model="form" ref="form" label-position="right">
                <div v-for="(question, index_q) in testPaper" :key="index_q"
                    style="width: 600px; margin:auto; padding: 1px 5px;">
                    <p>{{ question.content }} ({{ question.point }}分)</p>
                    <div v-show="question.type == 'singleChoice' || question.type == 'trueOrFalse'" style="
                        text-align: left;
                        padding-left: 50px;
                    ">
                        <el-form-item :prop="`questions[${index_q}].answer`"
                            :rules="{ required: true, message: '请选择选项', trigger: 'change' }">
                            <el-radio-group v-model="form.questions[index_q].answer">
                                <div v-for="answer in question.answers">
                                    <el-radio :label="answer.id.toString()">{{ answer.content
                                    }}</el-radio>
                                </div>
                            </el-radio-group>
                        </el-form-item>
                    </div>

                    <div v-show="question.type == 'shortAnswer'">
                        <el-form-item :prop="`questions[${index_q}].answer`"
                            :rules="{ required: true, message: '请填写主观题', trigger: 'blur' }">
                            <el-input type="textarea" :rows="2" v-model="form.questions[index_q].answer" placeholder="请做答" style="width: 60%;"></el-input>
                        </el-form-item>
                    </div>

                    <!-- 分割线 -->
                    <el-divider></el-divider>
                </div>
                <el-form-item>
                    <el-button type="primary" @click="submitForm('form')">交 卷</el-button>
                </el-form-item>
            </el-form>
        </el-col>
        <el-col :span="4"></el-col>
    </el-row>
</template>

<script>
import cookie from 'js-cookie'
import axios from 'axios'

export default {
    data() {
        return {
            testPaper: [],
            form: {
                exam_id: '',
                questions: []
            },
            duration: 0,
        }
    },
    methods: {
        submitForm(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    console.log('fuck1')
                    this.$confirm('确认交卷?', '提示', {
                        confirmButtonText: '是',
                        cancelButtonText: '否',
                        type: 'warning'
                    }).then(() => {
                        this.postPaper()
                    }).catch(() => {
                        alert('已取消交卷!');
                    })
                }
                else {
                    console.log('error submit!!');
                    return false;
                }
            });
        },
        handleProgress(data) {
            if (data.totalSeconds == 1) {
                this.postPaper()
            }
        },
        postPaper() {
            const token = cookie.get('jwt')
            axios.post('/wrong/myExam', this.form, { headers: { 'Authorization': token } })
                .then(() => {
                    this.$router.push({ name: 'exam' })
                    this.$fullscreen.exit()
                })
                .catch(res => {
                    console.log("异常触发");
                    console.log(res); //发生错误时执行的代码
                })
        }

    },
    created() {
        let exam_id = this.$route.params.exam_id
        if (exam_id !== undefined) {
            const token = cookie.get('jwt')
            axios.get('/paper/' + exam_id, { headers: { 'Authorization': token } }).then(res => {
                this.testPaper = res.data.questions;
                // this.tableData = res.data;//将后台传递的数组赋值给定义的空数组
                this.form.exam_id = res.data.id; //给form表单初始化
                this.form.questions = []

                let duration = res.data.duration.split(':')
                this.duration = (+duration[0]) * 60 * 60 * 1000 + (+duration[1]) * 60 * 1000

                for (let i = 0; i < this.testPaper.length; i++) {
                    let question = this.testPaper[i]
                    this.form.questions.push({
                        'question_id': question.id,
                        'answer': '',
                        'type': question.type
                    })
                }
            }).catch(res => {
                console.log("异常触发");
                console.log(res); //发生错误时执行的代码
            })
        }
        else {
            this.$router.push({ name: 'exam' })
        }
    }
}

</script>