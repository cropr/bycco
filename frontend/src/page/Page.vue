<template>

<v-app>

  <sidebar />
  <topbar />
  
  <v-content>
    <v-container v-show="!apiloaded">
      Just a moment. <v-progress-circular indeterminate />
    </v-container>
    <router-view :key="force" :ts="ts" v-if="apiloaded"/>
  </v-content>

  <bycco-footer />

  <v-snackbar v-model="snackbar" :color="color" bottom>
    {{ snacktext }}
    <template v-slot:action="{ attrs }">
      <v-btn text @click="snackbar = false" v-bind="attrs">
        <v-icon>cancel</v-icon>
      </v-btn>
    </template>
  </v-snackbar>

</v-app>

</template>

<script>
import { mapState } from "vuex"
import Swagger from "swagger-client"

import { processRoutes } from './router_page'
import { locales } from '@/util/lang'
import Sidebar from '@/components/Sidebar'
import Topbar from '@/components/Topbar'
import ByccoFooter from '@/components/ByccoFooter'

export default {

  name: 'Page',

  components: {
    Sidebar,
    Topbar,
    ByccoFooter,
  },

  data() {
    return {
      apiloaded: false,
      color: '',
      force: 0,
      locales: locales,
      snackbar: false,
      snacktext: '',
      ts: new Date(),            
    };
  },

  computed: {
    ...mapState(['locale', 'api', 'slug']),
  },

  methods: {

    getOpenApi() {
      let self = this;
      Swagger('/openapi.json').then(
        function(client){
          self.apiloaded = true;
          self.$store.commit('updateApi', client.apis.default);
          self.getRoutingTable()
        },
        function(data){
          console.error('could not fetch openapi.json', data)
          alert('Cannot load API');
        }
      );
    },

    getRoutingTable() {
      let self=this;
      let rt;
      console.log('api', this.api)
      this.api.anon_routingtable().then(
        function(data){
          self.routingtableloaded = true;
          console.log('got Routes', data.obj.routes)
          rt = processRoutes(data.obj.routes)
          self.$router.addRoutes(rt);
          let newroute = '/page/' + self.slug + '/' + self.locale;
          console.log('rt added', rt)
          console.log('going to', newroute)
          if (self.$route.path == newroute) {
            self.force++; 
          }
          else {
            self.$router.push(newroute)
          }
        },
        function(data){
          console.error('could not fetch routingtable', data).
          alert('Cannot load API');
        }
      )
    },

    showSnackbar(ev) {
      console.log('snackbar', ev);
      if (ev.text) {
        this.snacktext = ev.text;
        this.snackbar = true;
      }
      this.color =  ev.color ? ev.color : 'primary';
    },  
    
  },

  mounted() {
    let self=this;    
    this.getOpenApi();
    this.$root.$on('snackbar', this.showSnackbar);
    this.$router.beforeEach(function(to, from, next){
      console.log('processing url')
      let pparts = to.path.split('/');
      console.log('pparts', pparts)
      if (pparts.length == 4) {
        if (pparts[2] != self.slug) {
          self.$store.commit('updateSlug', pparts[2]);
        }
        if (pparts[3] != self.locale) {
          self.$store.commit('updateLocale', pparts[3]);
        }
      }
      next();
    })
  },  

}
</script>