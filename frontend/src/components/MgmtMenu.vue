<template>
<v-toolbar fixed dark dense app class="blue-grey darken-1">
  <v-toolbar-title>
    Administration
  </v-toolbar-title>
  <v-spacer></v-spacer>
  <v-toolbar-items>
    <v-btn flat large to="participants">Participants</v-btn>
    <v-btn flat large to="swar">Swar</v-btn>
  </v-toolbar-items>
</v-toolbar>
</template>

<script>
export default {

  name: "MgmtMenu",

}
</script>

<style scoped>
</style>