import Vue from 'vue'
import VueRouter from 'vue-router'
import store from './store/mgmt'
import { i18n } from './util/lang'
import './util/vuetify'
import './style/bycco.styl'

import MgmtTournament from './pages/MgmtTournament'
import MgmtTrns from './pages/MgmtTrns'
import MgmtParticipants from './pages/MgmtParticipants'
import MgmtSwar from './pages/MgmtSwar'

Vue.config.productionTip = false;

Vue.use(VueRouter);

const router = new VueRouter({
  routes: [
    {path: '/participants', component: MgmtParticipants},
    {path: '/trns', component: MgmtTrns},
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



