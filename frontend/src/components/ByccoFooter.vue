<template>
<v-footer height="auto" class="blue-grey lighten-1 white--text">
  <v-layout row class="py-2">
    <v-flex md3 sm6 xs12 class="ml-2" light>
      <a href="/bycco/us" v-t="'About Bycco'"></a>
    </v-flex>
    <v-flex md3 sm6 xs12 class="ml-2">
      <a href="/bycco/team" v-t="'The team'"></a>
    </v-flex>
    <v-flex md3 sm6 xs12 class="ml-2">
      {{ $t("Contact") }}: <a href="mailto:info@bycco.be">info@bycco.be</a>
    </v-flex>
    <v-flex md3 sm6 xs12 class="ml-2">
      <a href="https://www.facebook.com/ByccoBel">
        <img src="/static/img/facebook.png"></a>
      <a href="https://twitter.com/@ByccoBel">
        <img src="/static/img/twitter.png"></a>
    </v-flex>
  </v-layout>
</v-footer>
</template>

<script>
  export default {
    name: "ByccoFooter"
  }
</script>

<style scoped>

a:link, a:hover {
  color: white;
  text-decoration: none;
}

a:hover {
  font-weight: 700;
}

</style>