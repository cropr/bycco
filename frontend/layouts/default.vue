<template>
  <v-app>
    <v-navigation-drawer
      v-cloak
      v-model="drawer"
      app
      class="blue-grey darken-1"
    >
      <Sidebar />
    </v-navigation-drawer>
    <Topbar :drawer="drawer" @updateDrawer="updateDrawer" />
    <v-main>
      <nuxt />
    </v-main>
    <AdCarousel />
    <ByccoFooter />
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      drawer: false,
    }
  },

  methods: {
    updateDrawer(value) {
      this.drawer = value
    },
  },
}
</script>
