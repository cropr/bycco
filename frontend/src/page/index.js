import Vue from 'vue'
import vuetify from '@/plugins/vuetify';
import { i18n } from '@/util/lang'
import Page from './Page.vue'
import { router } from './router_page'
import store from './store_page'
import '@/assets/css/github-markdown.css'


window.vm = new Vue({
  vuetify,
  router,
  store,
  i18n,
  render: h => h(Page)
}).$mount('#app')

