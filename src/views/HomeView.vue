<template>
  <div class="HomeView container">
    <div class="login-wrapper">
      <div class="header">Login</div>
      <div class="form-wrapper">
        <input type="text" name="username" placeholder="username" class="input-item" v-model="username">
        <input type="password" name="password" placeholder="password" class="input-item" v-model="password"
          @keyup.enter="open">
        <div class="btn" @click="login()">Login</div>
      </div>
      <div class="msg">
        Don't have account?
        <a @click="dialogFormVisible = true" style="cursor: pointer;">Sign up</a>

        <!-- 注册表单 -->
        <el-dialog title="注册" :visible.sync="dialogFormVisible" append-to-body>
          <el-form :model="form" :rules="rules" ref="form" label-position="right">
            <el-form-item label="用户名" prop="account" :label-width="formLabelWidth">
              <el-input v-model="form.account" autocomplete="off" placeholder="account"></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="password" :label-width="formLabelWidth">
              <el-input v-model="form.password" autocomplete="off" placeholder="password"></el-input>
            </el-form-item>
            <el-form-item label="邮箱" prop="email" :label-width="formLabelWidth">
              <el-input v-model="form.email" autocomplete="off" placeholder="email"></el-input>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="dialogFormVisible = false">取 消</el-button>
            <el-button type="primary" @click="submitForm('form')">注 册</el-button>
          </div>
        </el-dialog>

      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import router from '@/router';

export default {
  name: 'HomeView',
  data() {
    return {
      username: 'zwt',
      password: 'zwt',
      dialogFormVisible: false,
      formLabelWidth: '120px',

      //表单数据
      form: {
        account: '',
        password: '',
        email: ''
      },

      //表单规则
      rules: {
        account: [
          { required: true, message: '请输入用户名称', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 8, max: 16, message: '长度在 8 到 16 个字符', trigger: 'blur' }
        ],
        email: [
          { required: true, message: '请输入邮箱', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }
        ]
      },
    }
  },
  methods: {
    //登录账号
    login() {
      axios.post("/api/tokens", {}, {
        auth: {
          'username': this.username,
          'password': this.password
        }
      }).then(res => {
        console.log(res.headers);
        this.$notify({
          title: '登录成功',
          message: '你好!' + this.username,
          type: 'success',
          position: 'bottom-right'
        });
        router.push({ path: 'user' }); //传值失败
      }).catch(reason => {
        console.log("异常触发");
        console.log(reason);
        this.$notify.error({
          title: '登录失败',
          message: '用户名或密码错误',
          position: 'bottom-right'
        });
      })
    },

    //注册账号
    add() {
      axios.post("http://localhost:5000/api/users/create", this.form).then(res => {
        alert('注册成功!');
        this.dialogFormVisible = false;
      }).catch(reason => {
        console.log("异常触发");
        console.log(reason);
      })
    },

    //表单输入限制
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.add()
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
  }
}
</script>

<style>
.container {
  height: 100%;
  background-image: linear-gradient(to right, #fbc2eb, #a6c1ee);
}

.login-wrapper {
  background-color: #fff;
  width: 358px;
  height: 500px;
  border-radius: 15px;
  padding: 0 50px;
  position: relative;
  left: 50%;
  top: 300px;
  transform: translate(-50%, -50%);
}

.header {
  font-size: 38px;
  font-weight: bold;
  text-align: center;
  line-height: 200px;
}

.input-item {
  display: block;
  width: 100%;
  margin-bottom: 20px;
  border: 0;
  padding: 10px;
  border-bottom: 1px solid rgb(128, 125, 125);
  font-size: 15px;
  outline: none;
}

.input-item:placeholder {
  text-transform: uppercase;
}

.btn {
  text-align: center;
  padding: 10px;
  width: 100%;
  margin-top: 40px;
  background-image: linear-gradient(to right, #a6c1ee, #fbc2eb);
  color: #fff;
  cursor: pointer;
}

.msg {
  text-align: center;
  line-height: 88px;
}

a {
  text-decoration-line: none;
  color: #abc1ee;
}
</style>
