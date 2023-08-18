import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import VueFullscreen from 'vue-fullscreen';
import VueCountdown from '@chenfengyuan/vue-countdown'

Vue.use(ElementUI);
Vue.use(VueFullscreen);
Vue.component(VueCountdown.name, VueCountdown)
Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
