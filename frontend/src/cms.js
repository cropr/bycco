import 'babel-polyfill';
import Vue from 'vue';
import Vuetify from 'vuetify';
import './stylus/bycco.styl';

Vue.use(Vuetify, {
  theme: {
    primary: "#78909C",
    secondary: "#B0BEC5",
    accent: "#0097A7",
    error: "#FF5252",
    warning: "#FFCA28",
    info: "#2196f3",
    success: "#4caf50"
  }
});

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
