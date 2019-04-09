import Vue from 'vue'
import store from './store'
import { i18n } from './util/lang'
import './util/vuetify'
import './style/bycco.styl'

import TrnSubscription from './pages/TrnSubscription'
import TrnParticipants from './pages/TrnParticipants'
import TrnView from './pages/TrnView'

Vue.config.productionTip = false;

window.application = {
  Vue: Vue,
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
  case 'TrnView':
    window.application.App = TrnView;
    break;
}


