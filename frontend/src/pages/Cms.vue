<template>
  <v-app>
    <sidebar />
    <topbar />
    <banner v-if="landing" />
    <v-content :class="{landing: landing}">
      <v-container fluid>
        <div class="mainarea my-1 pa-2">
          <cms-content></cms-content>
          <!--<cms-language-block></cms-language-block>-->
        </div>
      </v-container>
    </v-content>
    <ad-carousel />
    <bycco-footer />
  </v-app>
</template>

<script>

import { loadLanguageAsync } from '../util/lang'

import Sidebar from '../components/Sidebar'
import Topbar from '../components/Topbar'
import ByccoFooter from '../components/ByccoFooter'
import Banner from '../components/Banner'
import AdCarousel from '../components/AdCarousel'

export default {

  name: 'Cms',

  data () {return {
    tabactive: 0,
    landing: window.config.landing,

  }},

  components: {
    'sidebar': Sidebar,
    'topbar': Topbar,
    'bycco-footer': ByccoFooter,
    'banner': Banner,
    'ad-carousel': AdCarousel,
  },

  created () {
    loadLanguageAsync(window.config.lang);
  },

}
</script>

<style scoped>
.landing.v-content {
  padding-top: 0px !important;
}
</style>