import 'babel-polyfill';
import Vue from 'vue';
import Vuetify from 'vuetify';
import './stylus/bycco.styl';

Vue.use(Vuetify);

import axios from 'axios';
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

function getQueryVariable(variable) {
  var query = window.location.search.substring(1);
  var vars = query.split('&');
  for (var i = 0; i < vars.length; i++) {
    var pair = vars[i].split('=');
    if (decodeURIComponent(pair[0]) == variable) {
      return decodeURIComponent(pair[1]);
    }
  }
  return null
}

window.vm = new Vue({
  el: '#app',
  data: {
    drawer: false,
    tabix: 0,
    categories: [8, 10, 12, 14, 16, 18, 20],
    cat: 8,
    girls: [],
    boys: []
  },
  methods: {
    photourl (p) {
      return '/api/photo/' + ((p && p.id) ? p.id : 0);
    },
    changecat (cat) {
      var filtered;
      this.cat = cat;
      axios.get('/api/attendees?count=999&cat=G' + this.cat).then(
        response => {
          filtered = [];
          response.data.attendees.forEach(function(p){
            if (p.confirmed) filtered.push(p)
          });
          this.girls = filtered;
        }
      );
      axios.get('/api/attendees?count=999&cat=B'+ this.cat).then(
        response => {
          filtered = [];
          response.data.attendees.forEach(function(p){
            if (p.confirmed) filtered.push(p)
          });
          this.boys = filtered;
        }
      )

    }
  },

  mounted () {
    var qcat = getQueryVariable('cat'), self=this;
    console.log('qcat', qcat, this);
    console.log('theme primary', this.$vuetify.theme.primary)
    this.categories.forEach(function(c, ix){
      if (c == qcat) self.tabix = ix;
    });
    this.changecat(qcat ? qcat : this.cat);
  }

});
