<template>

<v-app>

  <v-app-bar v-cloak fixed dark app class="deep-purple darken-2" >
    <v-toolbar-items class="hidden-sm-and-down">
      <v-btn text large href="/">Management Bycco</v-btn>
    </v-toolbar-items>
    <v-spacer></v-spacer>
    <v-toolbar-items >
      <v-btn text large to="/pages">Pages</v-btn>
    </v-toolbar-items>
  </v-app-bar>

  <v-content>
    <router-view></router-view>
  </v-content>
  
  <v-footer color="blue-grey lighten-1" dark class="mt-2 pa-2">
    Website by <a target="_blank" href="https://www.chessdevil.net">
    Chessdevil Consulting</a>. &copy; 2018 - 2020.  All rights reserved
  </v-footer>  

</v-app>

</template>

<script>
// import {mapState} from "vuex"


export default {

  name: 'Mgmt',

  data () {return {
  }},


}
</script>

<style scoped>
</style>
