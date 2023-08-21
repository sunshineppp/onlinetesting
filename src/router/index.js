import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import UserView from '../views/UserView.vue'
import Permissions from '../components/Permissions.vue'
import Exam from '../components/Exam.vue'
import Questions from '../components/Questions.vue'
import TextPaper from '../components/TextPaper.vue'
import Synopsis from '../components/Synopsis.vue'
import Teacher from '../components/Teacher.vue'
import text from '../components/text.vue'
import EditPaper from '@/components/EditPaper.vue'
import ExamView from '@/components/ExamView.vue'
import TeacherView from '@/components/TeacherView.vue'
import Statistics from '@/components/Statistics.vue'
import MyExamScore from '@/components/MyExamScore.vue'
import MyExamScoreView from '@/components/MyExamScoreView.vue'

//防止push重复跳转同一个路由
const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}

Vue.use(VueRouter)

const routes = [
  //设置默认路由
  {
    path: '/',
    redirect: '/home'
  },
  {
    path: '/user',
    redirect: '/user/synopsis'
  },

  {
    path: '/home',
    name: 'home',
    component: HomeView
  },
  {
    path: '/user',
    name: 'user',
    component: UserView,
    children: [
      {
        path: 'permissions',
        component: Permissions
      },
      {
        path: 'exam',
        name: 'exam',
        component: Exam
      },
      {
        path: 'questions',
        component: Questions
      },
      {
        path: 'textPaper',
        name: 'textPaper',
        component: TextPaper
      },
      {
        path: 'textPaper/create',
        name: 'createPaper',
        component: EditPaper
      },
      {
        path: 'textPaper/update/:paper_id',
        name: 'updatePaper',
        component: EditPaper
      },
      {
        path: 'synopsis',
        component: Synopsis
      },
      {
        path: 'teacher',
        name: 'teacher',
        component: Teacher
      },
      {
        path: 'teacherView/:user_id/:testpaper_id_',
        name: 'teacherView',
        component: TeacherView
      },
      {
        path: 'statistics',
        component: Statistics
      },
      {
        path: 'myExamScore',
        component: MyExamScore
      },
      {
        path: 'myExamScoreView',
        name: 'myExamScoreView',
        component: MyExamScoreView
      },

      // 测试
      {
        path: 'text',
        component: text
      }

    ]
  },
  {
    path: '/exam/:exam_id',
    name: 'takeExam',
    component: ExamView
  },
]

const router = new VueRouter({
  // mode: 'history',
  // base: process.env.BASE_URL,
  routes
})

export default router
