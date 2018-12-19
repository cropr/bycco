<template>
  <v-app>
    <sidebar />
    <topbar />
    <mgmt-menu />
    <router-view :key="$route.fullPath"></router-view>
    <bycco-footer />
  </v-app>
</template>

<script>

import Sidebar from '../components/Sidebar'
import Topbar from '../components/Topbar'
import ByccoFooter from '../components/ByccoFooter'

export default {

  name: 'Adm',

  data () {return {
    title: 'Admin section'
  }}

  components: {
    'sidebar': Sidebar,
    'topbar': Topbar,
    'bycco-footer': ByccoFooter,
    'ad-carousel': AdCarousel,
  },

}
</script>

<style scoped>

</style>