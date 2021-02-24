<template>

<v-app>

  <sidebar />
  <topbar />
  
  <v-main>
    <router-view :key="$route.fullPath"  v-if="apiloaded" />
  </v-main>

  <ad-carousel />

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
import Swagger from "swagger-client"
import { mapState } from "vuex"
import { api, locales, setLanguage } from '@/util/server_injected'

import Sidebar from '@/components/Sidebar'
import Topbar from '@/components/Topbar'
import AdCarousel from '@/components/AdCarousel'
import ByccoFooter from '@/components/ByccoFooter'

export default {

  name: 'Page',

  components: {
    Sidebar,
    Topbar,
    ByccoFooter,
    AdCarousel
  },

  data() {
    return {
      apiloaded: false,
      color: '',
      locales: locales,
      snackbar: false,
      snacktext: '',            
    };
  },

  computed: {
    ...mapState(['locale', 'api', 'slug']),
  },

  methods: {

    getOpenApi() {
      let self = this;
      Swagger({spec: api}).then(
        function(client){
          self.$store.commit('updateApi', client.apis.default);
          self.apiloaded = true;
        },
        function(data){
          console.error('could not fetch openapi.json', data)
          alert('Cannot load API');
        }
      );
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
    let self=this, 
        routeparts = this.$route.path.split('/');
    console.log('mounting', routeparts, api)
    this.getOpenApi();
    this.$root.$on('snackbar', this.showSnackbar);
    this.$router.beforeEach(function(to, from, next){
      routeparts = to.path.split('/');
      console.log('before ', routeparts)
      if (routeparts[1] == 'page') {
        if (routeparts[2] != self.slug) {
          self.$store.commit('updateSlug', routeparts[2]);
        }
        if (routeparts[3] != self.locale) {
          self.$store.commit('updateLocale', routeparts[3]);
        }
      }
      next()
    });
    if (routeparts[0] == "") {
      this.$router.push('/page/home/en');
      return
    }
    console.log('mounted', routeparts);
    if (routeparts.length > 2) {
      if (routeparts[2] != self.slug) {
        self.$store.commit('updateSlug', routeparts[2]);
      }
    }
    if (routeparts.length > 3) {
          if (routeparts[3] != self.locale) {
        self.$store.commit('updateLocale', routeparts[3]);
      }
    }
    // setLanguage(this.locale)
  },  

}
</script>


