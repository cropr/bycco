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
    adCarouselValue: 0,
    nAdCarousel: 6,
  },
  methods: {
    gotoUrl (url) {
      console.log('going to ', url)
    },
    clickedMenu (item) {
      console.log('clicked menu', item)
    }
  },

  mounted () {
    var secCarousel = Math.floor((new Date()/1000) % (6 * this.nAdCarousel));
    this.adCarouselValue = Math.floor(secCarousel / this.nAdCarousel);
  }
});


window.config = {
  apiurl: '/api'
};

window.bridge = {

  gotoAngularRoute: function(path) {
    console.log('This will be overwritten by the angular bidge factory')
  },

  api: apicall,

};
