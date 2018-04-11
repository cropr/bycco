import 'babel-polyfill';
import apicall from './api/api';
import Vue from 'vue';
import Vuetify from 'vuetify';
import './stylus/bycco.styl';

Vue.use(Vuetify);


import MgAttendee from './components/MgAttendee';
import AdCarousel from './components/AdCarousel';

new Vue({
  el: '#app',
  data () {
    return {
      drawer: false,
    }
  },
  components: {
    "mg-attendee": MgAttendee,
    "ad-carousel": AdCarousel,
  },
});


