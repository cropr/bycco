<template>
<v-app-bar v-cloak fixed dark app class="deep-purple darken-2" >
  <v-app-bar-nav-icon @click.stop="openDrawer" />
  <v-toolbar-items>
    <v-btn text large href="/">Management</v-btn>
  </v-toolbar-items>
  <v-spacer></v-spacer>
  <v-toolbar-items class="hidden-sm-and-down">
    <v-btn text large href="/info/calendar">Pages </v-btn>
  </v-toolbar-items>
</v-app-bar>
</template>

<script>
export default {

  name: "Topbar",

  methods:   {
    openDrawer () {
      this.$store.commit('updateDrawer', true)
    },
  },
}
</script>

<style scoped>

</style>