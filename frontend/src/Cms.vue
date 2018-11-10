<template>
  <v-app>
    <sidebar />
    <topbar />
    <v-content>
      <v-container fluid>
        <div class="mainarea my-1 pa-2">
          <cms-content></cms-content>
          <!--<cms-language-block></cms-language-block>-->
        </div>
      </v-container>
    </v-content>
    <bycco-footer />
  </v-app>
</template>

<script>

import { loadLanguageAsync } from './util/lang'


import Sidebar from './components/Sidebar'
import Topbar from './components/Topbar'
import ByccoFooter from './components/ByccoFooter'
// import AdCarousel from './components/AdCarousel'

export default {

  name: 'Cms',

  data () {return {
    tabactive: 0,
  }},

  components: {
    'sidebar': Sidebar,
    'topbar': Topbar,
    'bycco-footer': ByccoFooter,
    // 'ad-carousel': AdCarousel,
  },

  created () {
    loadLanguageAsync(window.config.lang);
  },

}
</script>

<style scoped>

</style>