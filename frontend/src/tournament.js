import Vue from 'vue'
import store from './store'
import { i18n } from './util/lang'

import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
Vue.use(Vuetify);

import TrnSubscription from './pages/TrnSubscription'
import TrnParticipants from './pages/TrnParticipants'
import VueCmsPatch from "./vue-djangocms-patch";

Vue.config.productionTip = false;

window.application = {
  Vue: Vue,
  VueCmsPatch: VueCmsPatch,
  // App: Subscribe,
  store: store,
  i18n: i18n,
};

switch (window.config.appname) {
  case 'TrnSubscription':
    window.application.App = TrnSubscription;
    break;
  case 'TrnParticipants':
    window.application.App = TrnParticipants;
    break;
}


