import Vue from 'vue'
import VueRouter from 'vue-router'
import store from './store/mgmt'
import { i18n } from './util/lang'
import './util/vuetify'
import './style/bycco.styl'

import MgmtTournament from './pages/MgmtTournament'

Vue.config.productionTip = false;

const router = new VueRouter({
  routes: [
    {path: '/participants', component: MgmtPartipants},
    {path: '/swar', component: MgmtSwar},
    {path: '*', redirect: '/participants'},
  ],
  mode: 'hash',
});

window.application = {
  Vue: Vue,
  App: MgmtTournament,
  store: store,
  i18n: i18n,
  router,
};



