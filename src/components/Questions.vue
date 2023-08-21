<template>
  <div class="questions">

    <el-header style="background-color: #fff;">
      <!-- dialogForm -->
      <div style="margin-right: 10px; text-align: right;">
        <el-button type="primary" round @click="resetForm2()">添加</el-button>
      </div>
    </el-header>

    <!-- 表单 -->
    <el-dialog :title=type :visible.sync="dialogFormVisible" append-to-body>
      <el-form :model="form" :rules="rules" ref="form" label-position="right">
        <el-form-item label="题型" prop="type">
          <el-select v-model="form.type" placeholder="请选择题型">
            <el-option label="选择题" value="singleChoice"></el-option>
            <el-option label="判断题" value="trueOrFalse"></el-option>
            <el-option label="主观题" value="shortAnswer"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="题干" prop="content">
          <el-input v-model="form.content" autocomplete="off" placeholder="content"></el-input>
        </el-form-item>

        <!-- <template v-for="answer in form.answers">
          <el-form-item label="" prop="answer">
            <el-input v-model="answer.content" autocomplete="off" placeholder="answer"></el-input>
          </el-form-item>
        </template> -->

        <template v-for="(item, index) in form.answers">
          <el-form-item label="选项" prop="item" v-show="form.type == 'singleChoice'">
            <el-input v-model="form.answers[index].content" autocomplete="off" placeholder="answer"></el-input>
          </el-form-item>
        </template>

        <el-form-item label="答案：" prop="radio" v-if="form.type != 'shortAnswer'">
          <el-radio-group v-model="form.radio" v-show="form.type == 'singleChoice'">
            <el-radio :label=0>A</el-radio>
            <el-radio :label=1>B</el-radio>
            <el-radio :label=2>C</el-radio>
            <el-radio :label=3>D</el-radio>
          </el-radio-group>
          <el-radio-group v-model="form.radio" v-show="form.type == 'trueOrFalse'">
            <el-radio :label=0>true</el-radio>
            <el-radio :label=1>false</el-radio>
          </el-radio-group>
        </el-form-item>

        <template v-for="(item, index) in form.answers">
          <el-form-item label="答案" prop="" v-show="form.type == 'shortAnswer'">
            <el-input v-model="form.answers[index].content" autocomplete="off" placeholder="answer"></el-input>
          </el-form-item>
        </template>

        <el-form-item label="解析" prop="analysis">
          <el-input v-model="form.analysis" autocomplete="off" placeholder="analysis"></el-input>
        </el-form-item>
        <el-form-item label="难度" prop="level">
          <el-select v-model="form.level" placeholder="请选择难度">
            <el-option label="简单" value="easy"></el-option>
            <el-option label="中等" value="medium"></el-option>
            <el-option label="困难" value="hard"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="分值" prop="point">
          <el-input v-model="form.point" autocomplete="off" placeholder="point"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="resetForm('form')">取 消</el-button>
        <el-button type="primary" @click="submitForm('form')">确 定</el-button>
      </div>
    </el-dialog>

    <!-- slice(a,b)的作用是从已有的数组中返回选定的元素"a"表示开始，"b"表示结束。 -->
    <el-table :data="tableData.slice((currentPage - 1) * pageSize, currentPage * pageSize)" @row-click="handle" style="width: 100%;
      margin: auto;
      margin: 10px 0px;
      box-shadow: 0px 5px 10px rgba(0, 0, 0, .12), 0px 5px 10px rgba(0, 0, 0, .04); " max-height="500">

      <el-table-column prop="content" label="题干" width="450">
      </el-table-column>
      <el-table-column prop="type_2" label="题型" width="100">
      </el-table-column>
      <el-table-column prop="level" label="难度" width="100">
      </el-table-column>
      <el-table-column prop="point" label="分值" width="100">
      </el-table-column>
      <el-table-column fixed="right" label="操作" width="200">
        <template slot-scope="scope">
          <el-button-group>
            <el-button size="medium" plain icon="el-icon-edit" @click="Revise">修改</el-button>
            <el-button size="medium" type="danger" plain icon="el-icon-delete" @click="Delete">删除</el-button>
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

  </div>
</template>
  
<script>
import axios from 'axios'
import cookie from 'js-cookie'
import { mapActions } from 'vuex'

const questionLevelMap = new Map()
questionLevelMap.set('easy', '简单')
questionLevelMap.set('medium', '中等')
questionLevelMap.set('hard', '困难')

export default {
  name: 'questions',
  data() {
    return {
      isWatch: '',
      id: '',
      type: '',
      tableData: [],
      dialogFormVisible: false,
      currentPage: 1, // 当前页码
      pageSize: 5, // 每页的数据条数

      form: {
        content: '', //题干
        answers: '', //答案
        analysis: '', //题目解析
        type: '',
        level: '',
        point: '',
        id: '',
        radio: ''
      },

      //表单规则
      rules: {
        content: [
          { required: true, message: '请输入题干信息', trigger: 'blur' }
        ],
        answers: [
          { required: true, message: '请输入信息', trigger: 'blur' }
        ],
        analysis: [
          { required: true, message: '请输入题目解析', trigger: 'blur' },
        ],
        type: [
          { required: true, message: '请选择题型', trigger: 'change' }
        ],
        level: [
          { required: true, message: '请选择难度', trigger: 'change' }
        ],
        point: [
          { required: true, message: '请输入题目分值', trigger: 'blur' }
        ],
        radio: [
          { required: true, message: '请选择正确答案', trigger: 'change' }
        ]
      },
    }
  },
  methods: {
    //获取试题信息
    getTabelInfo() {
      const token = cookie.get('jwt')
      axios.get('/question/', {headers: {'Authorization': token}}).then(res => {
        // console.log(res.data);
        this.tableData = res.data;//将后台传递的数组赋值给定义的空数组
        for (let i in this.tableData) {
          this.tableData[i].type_2 = this.typeName(this.tableData[i].type);
          this.tableData[i].level = questionLevelMap.get(this.tableData[i].level)
        }
        // console.log(this.tableData)//检查一下数组内是否有数据
      }).catch(res => {
        console.log("异常触发");
        console.log(res);//发生错误时执行的代码
      })
    },

    addQuestions() {
      const token = cookie.get('jwt')
      axios.post('/question/create', this.form, {headers: {'Authorization': token}}).then(res => {
        alert('添加成功!');
        this.getTabelInfo();
        this.dialogFormVisible = false;
      }).catch(res => {
        console.log("异常触发");
        console.log(res);//发生错误时执行的代码
      })
    },

    //修改试题
    reviseQuestions(id) {
      const token = cookie.get('jwt')
      axios.post('/question/update/' + id, this.form, {headers: {'Authorization': token}}).then(res => {
        alert('修改成功!');
        this.getTabelInfo();
        this.dialogFormVisible = false;
      }).catch(res => {
        console.log("异常触发");
        console.log(res);
      })
    },

    //删除试题
    deleteQuestions(id) {
      const token = cookie.get('jwt')
      console.log(this.id);
      axios.delete('/question/delete/' + id, {headers: {'Authorization': token}}).then(res => {
        alert('删除成功!');
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
          console.log(this.form);
          if (this.type == "Add") {
            console.log("Add");
            this.addQuestions();
          }
          else {
            console.log("Revise");
            console.log(this.id);
            this.reviseQuestions(this.id);
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
      this.form.radio = '';
    },

    //点击添加按钮清空form
    resetForm2() {
      this.form.analysis = this.form.answers = this.form.content = this.form.id = this.form.level = this.form.point = this.form.type = '';
      this.dialogFormVisible = true;
      this.type = 'Add';
    },

    handle(row) {
      this.isWatch = 1; // 阻止点击表格行赋值时触发watch，使选项不为空

      this.id = row.id;
      this.form.analysis = row.analysis;
      this.form.answers = row.answers;
      this.form.content = row.content;
      this.form.level = row.level;
      this.form.point = row.point;
      this.form.type = row.type;
      // this.form = row;
      // console.log(this.form.answers);
      // console.log(this.form.answers[0].content)

    },

    Add() {
      this.type = "Add";
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
        this.deleteQuestions(this.id);
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
    },

    //判别类型名称
    typeName(type) {
      switch (type) {
        case ("singleChoice"): return "选择题"; break;
        case ("trueOrFalse"): return "判断题"; break;
        case ("shortAnswer"): return "主观题"; break;
      }
    },
  },
  mounted() {
    this.getTabelInfo(); //每次加载组件获取试卷信息
  },
  watch: {
    // 每当 form.type 改变时，这个函数就会执行
    "form.type"(newQuestion, oldQuestion) {
      if (this.isWatch) {
        this.isWatch = 0; //允许watch
        return 0;
      }
      if (this.form.type == "singleChoice") {
        this.form.answers = [
          {
            "content": 'A.',
            "correct": 0,
            "id": ''
          },
          {
            "content": 'B.',
            "correct": 0,
            "id": ''
          },
          {
            "content": 'C.',
            "correct": 0,
            "id": ''
          },
          {
            "content": 'D.',
            "correct": 0,
            "id": ''
          },
        ]
      } else if (this.form.type == "trueOrFalse") {
        this.form.answers = [
          {
            "content": 'true',
            "correct": 0,
            "id": ''
          },
          {
            "content": 'false',
            "correct": 0,
            "id": ''
          }
        ]
      } else {
        this.form.answers = [
          {
            "content": '',
            "correct": 1,
            "id": ''
          }
        ]
      }
    },
    radio(newQuestion, oldQuestion) {
      if (this.form.radio != '') {
        this.form.answers[this.form.radio].correct = 1;
      }
    },
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
  