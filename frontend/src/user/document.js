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
import store from '@/user/store'
import App from '@/user/Document.vue'
import router from '@/user/router'
import {start, getDocContent, changeSlug, changeLocale} from '@/util/docpage'
import {setNavigation} from '@/util/utils'

setNavigation('getDocContent', getDocContent)
setNavigation('changeSlug', changeSlug)
setNavigation('changeLocale', changeLocale)

let vm = new Vue({
  vuetify,
  store,
  i18n,
  router, 
  render: h => h(App),
}).$mount('#app')

start(vm);