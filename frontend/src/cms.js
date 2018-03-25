import 'babel-polyfill';
import Vue from 'vue';
import Vuetify from 'vuetify';
import './stylus/bycco.styl';

Vue.use(Vuetify);

new Vue({
  el: '#app',
  data: {
    drawer: false,
    adCarouselValue: 0,
    nAdCarousel: 5,
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
