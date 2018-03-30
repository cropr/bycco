import 'babel-polyfill';
import apicall from './api/api';
import Vue from 'vue';
import Vuetify from 'vuetify';
import './stylus/bycco.styl';

Vue.use(Vuetify);

var vm = new Vue({
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

window.config = {
  apiurl: '/api'
};

window.bridge = {

  gotoAngularRoute: function(path) {
    console.log('This will be overwritten by the angular bridge factory')
  },

  api: apicall,

};

