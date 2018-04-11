import 'babel-polyfill';
import Vue from 'vue';
import Vuetify from 'vuetify';
import './stylus/bycco.styl';
import apicall from './api/api';

Vue.use(Vuetify);

import ViewTrn from './components/ViewTrn';
import AdCarousel from './components/AdCarousel';

new Vue({
  el: '#app',
  data () {
    return {
      drawer: false,
    }
  },
  components: {
    "view-trn": ViewTrn,
    "ad-carousel": AdCarousel,
  },
});


