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
    <Topbar landing="landing" :drawer="drawer" @updateDrawer="updateDrawer" />
    <v-main>
      <v-parallax
        v-if="$vuetify.breakpoint.mdAndUp"
        :src="require('~/assets/pier_big.jpg')"
        height="400"
      />
      <v-parallax
        v-if="$vuetify.breakpoint.sm"
        :src="require('~/assets/pier_medium.jpg')"
        height="300"
      />
      <v-parallax
        v-if="$vuetify.breakpoint.xs"
        :src="require('~/assets/pier_small.jpg')"
        height="200"
      />
      <nuxt />
      <v-parallax
        v-if="$vuetify.breakpoint.smAndUp"
        :src="require('~/assets/winnaars_big.jpg')"
        height="400"
      />
      <v-parallax
        v-if="$vuetify.breakpoint.xs"
        :src="require('~/assets/winnaars_small.jpg')"
        height="200"
      />
      <AdCarousel />
      <ByccoFooter />
    </v-main>
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

<style></style>
