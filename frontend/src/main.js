import Vue from 'vue';
import Vuetify from 'vuetify';
import App from './app.vue';
import './stylus/main.styl'

Vue.use(Vuetify);

new Vue({
  el: '#app',
  data: {
      drawer: false,
  },
  methods: {
    toggleMenu () {
      this.drawer = !this.drawer;
    },
    gotoUrl (url) {
      console.log('going to ', url)
    },
    clickedMenu (item) {
      console.log('clicked menu', item)
    }
  }
});
