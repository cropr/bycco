import Vue from 'vue';
import Vuetify from 'vuetify';

import 'angular/angular.min';
import 'angular-animate/angular-animate.min';
import 'angular-aria/angular-aria.min';
import 'angular-material/angular-material';
import 'angular-sanitize/angular-sanitize.min';
import 'ng-file-upload/dist/ng-file-upload.min';
import 'ui-cropper/compile/minified/ui-cropper';

import './angular/api';
import './angular/apidef';
import './angular/ctrl_sub';

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
