import Vue from 'vue'
// import Store from './store'
import { i18n } from './util/lang'

// import Vuetify from 'vuetify'
// import 'vuetify/dist/vuetify.min.css'
// Vue.use(Vuetify);

import Subscribe from './Subscribe.vue'

Vue.config.productionTip = false;

window.application = {
  Vue: Vue,
  App: Subscribe,
  // Store: Store,
  I18n: i18n,
};



