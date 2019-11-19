import Vue from 'vue'
import vuetify from '@/plugins/vuetify';

window.config = window.config || {};
window.config.api_url =  process.env.VUE_APP_API_URL;

import store from '@/store/store_mgmt'
import App from './Mgmt.vue'

let vm = new Vue({
  vuetify,
  store,
  render: h => h(App),
}).$mount('#app')

