<template>
    <el-form :model="form" label-position="right">
        <template v-for="(question, index_q) in testPaper">
            <p>{{ question.content }}</p>
            <div v-show="question.type == 'singleChoice' || question.type == 'trueOrFalse'">
                <el-radio-group v-model="form.questions[index_q].answer">
                    <el-radio v-for="answer in question.answers" :label="answer.id.toString()">{{ answer.content
                    }}</el-radio>
                </el-radio-group>
            </div>

            <div v-show="question.type == 'shortAnswer'">
                <el-input v-model="form.questions[index_q].answer" placeholder="请做答"></el-input>
            </div>
        </template>
        <el-form-item>
            <el-button type="primary" @click="submitForm">交 卷</el-button>
        </el-form-item>
    </el-form>
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
        }
    },
    methods: {
        submitForm() {
            console.log(this.form);
            this.$confirm('确认交卷?', '提示', {
                confirmButtonText: '是',
                cancelButtonText: '否',
                type: 'warning'
            }).then(() => {
                const token = cookie.get('jwt')
                axios.post('/wrong/myExam', this.form, { headers: { 'Authorization': token } })
                    .then(() => {
                        this.$router.push({name: 'exam'})
                    })
                    .catch(res => {
                        console.log("异常触发");
                        console.log(res); //发生错误时执行的代码
                    })
            }).catch(() => {
                alert('已取消交卷!');
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