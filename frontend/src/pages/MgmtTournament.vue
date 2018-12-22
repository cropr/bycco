<template>
  <v-app>
    <sidebar />
    <topbar />
    <mgmt-menu class="mgmtmenu"/>
    <v-content class="mgmtcontent">
      <router-view :key="$route.fullPath"></router-view>
    </v-content>
    <bycco-footer />
  </v-app>
</template>

<script>

import Sidebar from '../components/Sidebar'
import Topbar from '../components/Topbar'
import ByccoFooter from '../components/ByccoFooter'
import MgmtMenu from '../components/MgmtMenu'

export default {

  name: 'Adm',

  data () {return {
    title: 'Admin section'
  }},

  components: {
    Sidebar,
    Topbar,
    ByccoFooter,
    MgmtMenu,
    // 'ad-carousel': AdCarousel,
  },

}
</script>

<style scoped>
.mgmtmenu {
  margin-top: 64px !important;
}
.mgmtcontent {
  margin-top: 64px;
}

</style>