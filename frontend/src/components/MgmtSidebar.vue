<template>
  <v-navigation-drawer v-cloak dark app  v-model="drawer"
      class="navmax deep-purple darken-1" >
    <v-toolbar text class="deep-purple">
      <v-list>
        <v-list-item>
          <v-list-item-title class="title">
            Menu
          </v-list-item-title>
        </v-list-item>
      </v-list>
    </v-toolbar>
    <v-divider></v-divider>
    <v-list dark dense class="deep-purple darken-1">
      <v-list-item href="/pages">
        <v-list-item-content>Pages</v-list-item-content>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script>

import { mapState } from 'vuex'

export default {

  name: "MgmtSidebar",

  computed: {
    drawer: {
      get () {
        return this.$store.state.drawer
      },
      set (value) {
        this.$store.commit('updateDrawer', value)
      }
    },
    ...mapState(['authenticated']),
  },

}

</script>

<style scoped>
</style>