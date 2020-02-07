<template>

<v-app>

  <v-app-bar v-cloak fixed dark app class="deep-purple darken-2" >
    <v-toolbar-items class="hidden-sm-and-down">
      <v-btn text large href="/mgmt">Management Bycco</v-btn>
    </v-toolbar-items>
    <v-spacer></v-spacer>
    <v-toolbar-items >
      <v-btn text large to="/mgmt/page/list">Pages</v-btn>
    </v-toolbar-items>
    <v-toolbar-items >
      <v-btn text large to="/mgmt/doc/list">Docs</v-btn>
    </v-toolbar-items>
    <v-toolbar-items >
      <v-btn text large to="/mgmt/participant/list">Participants</v-btn>
    </v-toolbar-items>
  </v-app-bar>

  <v-content>
    <router-view></router-view>
  </v-content>
  
  <v-footer color="blue-grey lighten-1" dark class="mt-2 pa-2">
    Website by <a target="_blank" href="https://www.chessdevil.net">
    Chessdevil Consulting</a>. &copy; 2018 - 2020.  All rights reserved
  </v-footer>
    <v-snackbar v-model="snackbar" bottom>
      {{ snacktext }} 
      <span v-show="reason">&nbsp;&nbsp; reason: {{ reason }}</span>
      <v-btn text @click="snackbar = false">
        <v-icon>cancel</v-icon>
      </v-btn>
    </v-snackbar> 

</v-app>

</template>

<script>
export default {

  name: 'Mgmt',

  data () { return {
    snackbar: false,
    snacktext: '',
    reason: null,
    text: '',
  }},

  mounted () {
    this.$root.$on('snackbar', function(ev) {
      console.log('received snackbar event', ev.text)
      if (ev.text) {
        this.snacktext = ev.text;
        this.reason = ev.reason;
        this.snackbar = true;
      }
    }.bind(this));
  }


}
</script>

<style scoped>
</style>
