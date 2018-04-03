import 'babel-polyfill';
import Vue from 'vue';
import Vuetify from 'vuetify';
import './stylus/bycco.styl';
import apicall from './api/api';

Vue.use(Vuetify);

import MgTrn from './components/MgTrn';
import AdCarousel from './components/AdCarousel';

window.config = {
  apiurl: '/api'
};

new Vue({
  el: '#app',
  data () {
    return {
      drawer: false,
    }
  },
  components: {
    "mg-trn": MgTrn,
    "ad-carousel": AdCarousel,
  },
});


