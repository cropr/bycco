import 'babel-polyfill';
import Vue from 'vue';
import Vuetify from 'vuetify';
import './stylus/bycco.styl';

import AdCarousel from './components/AdCarousel';

Vue.use(Vuetify);

new Vue({
  el: '#app',
  data: {
    drawer: false,
    lang: window.config.lang,
  },
  components: {
    "ad-carousel": AdCarousel,
  },
  methods: {
    gotoUrl (url) {
      console.log('going to ', url)
    },
    clickedMenu (item) {
      console.log('clicked menu', item)
    },
    _ls (dict) {  //
      if (this.lang in dict) return dict[this.lang];
      if ('def' in dict) return dict.def;
      return '***';
    },
    _lo (l) {
      return l == this.lang
    }

  },

});
