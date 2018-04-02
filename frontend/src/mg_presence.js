import 'babel-polyfill';
import Vue from 'vue';
import Vuetify from 'vuetify';
import './stylus/bycco.styl';
import apicall from './api/api';

Vue.use(Vuetify);

import MgPresence from './components/MgPresence';
import AdCarousel from './components/AdCarousel';

window.vm = new Vue({
  el: '#app',
  data: {
      drawer: false,
  },
  components: {
    "mg-presence": MgPresence,
    "ad-carousel": AdCarousel,

  },
});

window.config = {
  apiurl: '/api'
};

