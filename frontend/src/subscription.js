import 'babel-polyfill';
import Vue from 'vue';
import Vuetify from 'vuetify';
import './stylus/bycco.styl';
import apicall from './api/api';

Vue.use(Vuetify);

new Vue({
  el: '#app',
  data: {
    drawer: false,
  },
  methods: {
    gotoUrl (url) {
      console.log('going to ', url)
    },
    clickedMenu (item) {
      console.log('clicked menu', item)
    }
  },

});

window.bridge = {

  gotoAngularRoute: function(path) {
    console.log('This will be overwritten by the angular bridge factory')
  },

  api: apicall,

};
