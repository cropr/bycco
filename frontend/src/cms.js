console.log(1)

import Vue from 'vue'
import store from './store'
import { i18n } from './util/lang'
import VueCmsPatch from './vue-djangocms-patch';
import './util/vuetify'
import './style/bycco.styl'

import Cms from './pages/Cms.vue'

Vue.config.productionTip = false;

window.application = {
  Vue: Vue,
  App: Cms,
  store: store,
  i18n: i18n,
  VueCmsPatch: VueCmsPatch,
};

