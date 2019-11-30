import Vue from 'vue'
import vuetify from '@/plugins/vuetify';

// window.config must be configured before the store is loaded

window.config = window.config || {};
window.config.api_url =  process.env.VUE_APP_API_URL;

import {i18n} from '@/util/lang'
import store from '@/user/store'
import App from '@/user/Subscription.vue'
import router from '@/user/router'
import {start, getPageContent, changeSlug, changeLocale} from '@/util/nonpage'
import {setNavigation} from '@/util/utils'

setNavigation('getPageContent', getPageContent)
setNavigation('changeSlug', changeSlug)
setNavigation('changeLocale', changeLocale)


let vm=new Vue({
  vuetify,
  store,
  i18n,
  router, 
  render: h => h(App),
}).$mount('#app')

start(vm)
