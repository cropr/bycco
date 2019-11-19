import Vue from 'vue'
import vuetify from '@/plugins/vuetify';
import store from '../store/store_landingspage'
import {i18n, setLanguage} from '../util/lang'
import App from './pages/LandingsPage.vue'

Vue.config.productionTip = false

window.config = {
  api_url: process.env.VUE_APP_API_URL
}

let vm = new Vue({
  vuetify,
  store,
  i18n,
  render: h => h(App)
}).$mount('#app')
setLanguage(vm.$store.state.currentLocale)