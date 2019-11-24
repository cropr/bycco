import Vue from 'vue'
import vuetify from '@/plugins/vuetify';

window.config = window.config || {};
window.config.api_url =  process.env.VUE_APP_API_URL;

import store from '@/mgmt/store_mgmt'
import router from '@/mgmt/router_mgmt'
import App from '@/mgmt/Mgmt.vue'

new Vue({
  vuetify,
  store,
  router,
  render: h => h(App),
}).$mount('#app')

