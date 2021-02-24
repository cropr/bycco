import Vue from 'vue'
import vuetify from '@/util/vuetify';
import { i18n } from '@/util/server_injected'
import Page from '@/Page.vue'
import router from '@/router'
import store from '@/store'
import '@/assets/css/github-markdown.css'


window.vm = new Vue({
  vuetify,
  router,
  store,
  i18n,
  render: h => h(Page)
}).$mount('#app')
