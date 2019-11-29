import Vue from 'vue'
import vuetify from '@/plugins/vuetify';

// window.config must be configured before the store is loaded
// now fake the server side injection in landingpage.html in a dev environment

window.config = window.config || {};
window.config.api_url =  process.env.VUE_APP_API_URL;
if (process.env.NODE_ENV == 'development') {
  window.config.slug = 'home';
}

import {i18n} from '@/util/lang'
import store from '@/store/store_main'
import App from '@/pages/Page.vue'
import router from '@/views/router'
import { startPage } from '@/util/page'

let vm = new Vue({
  vuetify,
  store,
  i18n,
  router, 
  render: h => h(App),
}).$mount('#app')

startPage(vm);