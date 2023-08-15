import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import UserView from '../views/UserView.vue'
import Permissions from '../components/Permissions.vue'
import Exam from '../components/Exam.vue'
import Questions from '../components/Questions.vue'
import TextPaper from '../components/TextPaper.vue'
import Synopsis from '../components/Synopsis.vue'
import Mine from '../components/Mine.vue'
import text from '../components/text.vue'

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
        component: TextPaper
      },
      {
        path: 'synopsis',
        component: Synopsis
      },
      {
        path: 'mine',
        component: Mine
      },

      //
      {
        path: 'text',
        component: text
      }
    ]
  },
]

const router = new VueRouter({
  // mode: 'history',
  // base: process.env.BASE_URL,
  routes
})

export default router
