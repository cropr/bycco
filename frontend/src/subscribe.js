import Vue from 'vue'
import store from './store'
import { i18n } from './util/lang'

import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
Vue.use(Vuetify);

import Subscribe from './Subscribe.vue'
import VueCmsPatch from "./vue-djangocms-patch";

Vue.config.productionTip = false;

window.application = {
  Vue: Vue,
  VueCmsPatch: VueCmsPatch,
  App: Subscribe,
  store: store,
  i18n: i18n,
};



