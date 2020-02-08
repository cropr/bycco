<template>

<v-app>

  <sidebar />
  <topbar />
  <v-content>
    <router-view  :key="$route.fullPath" />
    <ad-carousel/>
    <bycco-footer />
  </v-content>

</v-app>

</template>

<script>

import Sidebar from '../components/Sidebar.vue'
import Topbar from '../components/Topbar.vue'
import ByccoFooter from '../components/ByccoFooter.vue'
import AdCarousel from '../components/AdCarousel.vue'

export default {

  name: 'Default',

  components: {
    Sidebar,
    Topbar,
    ByccoFooter,
    AdCarousel,
  },

}
</script>
