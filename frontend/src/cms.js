import Vue from 'vue'
import { i18n } from './util/lang'
import store from './store'
import marked from 'marked'
import VueCmsPatch from './vue-djangocms-patch';
import './util/vuetify'
import './style/bycco.styl'

import Cms from './pages/Cms.vue'

window.config.marked = marked;

Vue.config.productionTip = false;

window.application = {
  Vue: Vue,
  App: Cms,
  store: store,
  i18n: i18n,
  VueCmsPatch: VueCmsPatch,
};

