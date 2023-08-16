<template>
    <el-form :model="form" :rules="rules" ref="newPaper">
        <el-form-item label="考试名称" prop="name">
            <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="考试时长(分钟)" prop="duration">
            <el-input-number v-model="form.duration" :min="1" :max="240"></el-input-number>
        </el-form-item>
        <el-form-item label="试题">
            <el-table ref="questionTable" :data="questions" @selection-change="handleSelectionChange">
                <el-table-column type="selection"></el-table-column>
                <el-table-column prop="content" label="题干">
                </el-table-column>
                <el-table-column prop="type" label="题型">
                </el-table-column>
                <el-table-column prop="point" label="分值"></el-table-column>
            </el-table>
        </el-form-item>
        <el-form-item>
            <el-button v-if="this.$route.params.paper_id !== undefined" @click="show()" icon="el-icon-search">显示已选</el-button>
            <el-button type="primary" @click="submit('newPaper')">提交</el-button>
            <el-button @click="cancel()">取消</el-button>
        </el-form-item>
    </el-form>
</template>

<script>
import axios from 'axios'
import cookie from 'js-cookie'

const questionTypeMap = new Map()
questionTypeMap.set('singleChoice', '单选题')
questionTypeMap.set('trueOrFalse', '判断题')
questionTypeMap.set('shortAnswer', '简答题')

export default {
    name: 'PaperCreate',
    data() {
        return {
            form: {
                name: '',
                duration: 0,
            },
            questionID: [],
            oldQuestionID: [],
            questions: [],
            rules: {
                name: [{ required: true, message: '请输入考试名称', trigger: 'blur' }]
            }
        }
    },
    methods: {
        show() {
            this.questions.forEach(q => {
                if (this.oldQuestionID.includes(q.id)) {
                    this.$refs.questionTable.toggleRowSelection(q)
                }
            })
        },
        submit(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    if (this.questionID.length == 0) {
                        this.$notify({
                            title: '提交失败',
                            message: '题目不能为空',
                            type: 'warning'
                        })
                        return
                    }

                    let token = cookie.get('jwt')
                    let duration = new Date(0);
                    duration.setMinutes(this.form.duration)
                    let durationStr = duration.toISOString().substring(11, 19)

                    let paper_id = this.$route.params.paper_id
                    if (paper_id !== undefined) {
                        axios.post('/paper/edit/' + paper_id,
                            { 'name': this.form.name, 'duration': durationStr, 'questionID': this.questionID },
                            { headers: { 'Authorization': token } }
                        ).then(() => {
                            this.$notify({
                                title: '更新成功',
                                message: '成功修改试卷',
                                type: 'success'
                            })
                            this.$router.push({ name: 'textPaper' })
                        }).catch(err => {
                            console.log(err)
                        })
                    }
                    else {
                        axios.post('/paper/edit',
                            { 'name': this.form.name, 'duration': durationStr, 'questionID': this.questionID },
                            { headers: { 'Authorization': token } }
                        ).then(() => {
                            this.$notify({
                                title: '提交成功',
                                message: '成功创建新试卷',
                                type: 'success'
                            })
                            this.$router.push({ name: 'textPaper' })
                        }).catch(err => {
                            console.log(err)
                        })
                    }
                }
                else {
                    return false
                }
            })
        },
        cancel() {
            this.$router.push({ name: 'textPaper' })
        },
        handleSelectionChange(selected) {
            this.questionID = selected.map(q => {
                return q.id
            })
        }
    },
    created() {
        let token = cookie.get('jwt')
        axios.get('/question', { headers: { 'Authorization': token } })
            .then((response) => {
                this.questions = response.data.map((question) => {
                    question.type = questionTypeMap.get(question.type)
                    return question
                })

                let id = this.$route.params.paper_id
                if (id !== undefined) {
                    axios.get('/paper/info/'+id, {headers: {'Authorization': token}})
                        .then((res) => {
                            this.form.name = res.data.name
                            let duration = res.data.duration.split(':')
                            this.form.duration = (+duration[0]) * 60 + (+duration[1])
                            this.oldQuestionID = res.data.questionID
                        })
                        .catch(err => {console.log(err)})
                }
            })
            .catch((error) => {
                console.log(error)
            })

    }
}

</script>