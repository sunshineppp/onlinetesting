<template>
  <el-container class="user">

    <el-aside width="200px">
      <div style="height: 30px; padding: 15px 0px;"><b>在线考试系统</b></div>
      <el-menu :default-openeds="['1']">
        <el-submenu index="1">
          <template slot="title"><i class="el-icon-menu"></i>导航</template>
          <el-menu-item index="1-1" @click="gotoPermissions" v-if="permission_id == 3"><i
              class="el-icon-s-check"></i>用户管理</el-menu-item>
          <el-submenu index="1-2" v-if="permission_id == 3 || permission_id == 2">
            <template slot="title"><i class="el-icon-document"></i>考试管理</template>
            <el-menu-item index="1-2-1" @click="gotoQuestions"><i class="el-icon-document-checked"></i>试题管理</el-menu-item>
            <el-menu-item index="1-2-2" @click="gotoTextPaper"><i class="el-icon-document-checked"></i>试卷管理</el-menu-item>
            <el-menu-item index="1-2-3" @click="gotoTeacher"><i class="el-icon-edit"></i>试卷批改</el-menu-item>
            <el-menu-item index="1-2-4" @click="gotoStatistics"><i class="el-icon-pie-chart"></i>试卷统计</el-menu-item>
          </el-submenu>
          <el-submenu index="1-3" v-if="permission_id != 0">
            <template slot="title"><i class="el-icon-document"></i>我的考试</template>
            <el-menu-item index="1-3-1" @click="gotoExam"><i class="el-icon-monitor"></i>在线考试</el-menu-item>
            <el-menu-item index="1-3-2" @click="gotoMyExamScore"><i class="el-icon-data-analysis"></i>我的成绩</el-menu-item>
          </el-submenu>
        </el-submenu>
        <el-menu-item index="2" @click="gotoSynopsis">
          <template slot="title"><i class="el-icon-help"></i>简介</template>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header>
        <el-dropdown @command="gotoHome" trigger="click" style="margin-right: 15px;">
          <span class="el-dropdown-link">
            <i class="el-icon-user"></i>
            {{ account }}
            <i class="el-icon-arrow-down el-icon--right"></i>
          </span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item><i class="el-icon-switch-button"></i>退出</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </el-header>

      <el-main style="padding: 10px;">
        <router-view />
      </el-main>
    </el-container>

  </el-container>
</template>

<script>
import cookie from 'js-cookie'
import { decodeJwt } from 'jose'

export default {
  name: 'user',
  data() {
    return {
      account: '',
      permission_id: '',
      permission_name: ''
    }
  },
  methods: {
    gotoPermissions() {
      this.$router.push({ path: '/user/permissions' });
    },
    gotoExam() {
      this.$router.push({ path: '/user/exam' });
    },
    gotoQuestions() {
      this.$router.push({ path: '/user/questions' });
    },
    gotoTextPaper() {
      this.$router.push({ path: '/user/textPaper' });
    },
    gotoSynopsis() {
      this.$router.push({ path: '/user/synopsis' });
    },
    gotoTeacher() {
      this.$router.push({ path: '/user/teacher' });
    },
    gotoStatistics() {
      this.$router.push({ path: '/user/statistics' })
    },
    gotoMyExamScore() {
      this.$router.push({ path: '/user/myExamScore' });
    },
    gotoHome() {
      this.$router.push({ path: '/' });
    },
  },
  created() {
    let token = cookie.get('jwt')
    let payload = decodeJwt(token)
    // console.log(payload);
    // console.log(payload.account);
    // console.log(payload.permission_id);
    this.account = payload['account']; //用户名赋值
    this.permission_id = payload['permission_id']; //权限等级赋值

    //权限等级赋值
    // switch(payload.permission_id){
    //   case(0): this.permission_name = "游客"; break;
    //   case(1): this.permission_name = "学生"; break;
    //   case(2): this.permission_name = "教师"; break;
    //   case(3): this.permission_name = "超级管理员"; break;
    // }
  }
};
</script>

<style>
.el-container {
  height: 100%;
  border: 1px solid #eee;
}

.el-header {
  background-color: #B3C0D1;
  color: #333;
  line-height: 60px;
  text-align: right;
  font-size: 12px;
}

.el-aside {
  background-color: #D3DCE6;
  color: #333;
  text-align: center;
}

.el-main {
  background-color: #E9EEF3;
  color: #333;
  text-align: center;
  width: 100%;
}

.user {
  opacity: 0.9;
}
</style>