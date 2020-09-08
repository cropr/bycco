<template>

<v-app>

  <v-app-bar v-cloak dark app class="deep-purple darken-2" >
    <v-app-bar-nav-icon @click.stop="toggleDrawer()" />
    <v-toolbar-items>
      <v-btn text large href="/">FRBE-KBSB-KSB</v-btn>
    </v-toolbar-items>
    <v-spacer/>
    <v-toolbar-title>Admin Interface</v-toolbar-title>
  </v-app-bar>
  <v-navigation-drawer app v-model="drawer" dark v-cloak
      class="deep-purple" >
    <v-toolbar dark class="deep-purple">
      <v-list>
        <v-list-item>
          <v-list-item-title class="title">
            Menu
          </v-list-item-title>
        </v-list-item>
      </v-list>
    </v-toolbar>
    <v-list dark dense class="deep-purple">
      <v-list-item @click="goto('page/list')" >
          <v-list-item-icon>
            <v-icon>mdi-file</v-icon>
          </v-list-item-icon>
        <v-list-item-content>Pages</v-list-item-content>
      </v-list-item>
      <v-list-item @click="goto('file/list')" >
          <v-list-item-icon>
            <v-icon>mdi-file-document</v-icon>
          </v-list-item-icon>
        <v-list-item-content>Files</v-list-item-content>
      </v-list-item>
      <v-list-item @click="goto('bmember/list')" >
          <v-list-item-icon>
            <v-icon>mdi-account-multiple</v-icon>
          </v-list-item-icon>
        <v-list-item-content>Board Members</v-list-item-content>
      </v-list-item>
      <v-list-item @click="goto('brole/list')" >
          <v-list-item-icon>
            <v-icon>mdi-account-tie</v-icon>
          </v-list-item-icon>
        <v-list-item-content>Board Roles</v-list-item-content>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>

  <v-content>
    <router-view v-if="apiloaded"></router-view>
  </v-content>
  
  <v-snackbar v-model="snackbar" bottom>
    {{ snacktext }} 
    <span v-show="reason">&nbsp;&nbsp; reason: {{ reason }}</span>
    <v-btn text @click="snackbar = false">
      <v-icon>mdi-close</v-icon>
    </v-btn>
  </v-snackbar> 

</v-app>

</template>

<script>
import Swagger from 'swagger-client' 

export default {

  name: 'Mgmt',

  data () { return {
    apiloaded: false,
    drawer: false,
    snackbar: false,
    snacktext: '',
    reason: null,
    text: '',
  }},

  methods: {

    getOpenApi() {
      let self = this;
      Swagger('/openapi.json').then(
        function(client){
          self.apiloaded = true;
          self.$store.commit('updateApi', client.apis.default)
        },
        function(data){
          console.error('could not fetch openapi.json', data)
          alert('Cannot load API');
        }
      )
    },

    goto (p) {
      this.$router.push('/mgmt/' + p)
    },

    toggleDrawer () {
      this.drawer =  !this.drawer;
    },
    
  },

  mounted () {
    let self=this;
    this.$root.$on('snackbar', function(ev) {
      console.log('received snackbar event', ev.text)
      if (ev.text) {
        self.snacktext = ev.text;
        self.reason = ev.reason;
        self.snackbar = true;
      }
    });
    this.getOpenApi();
  }


}
</script>

<style scoped>
</style>
