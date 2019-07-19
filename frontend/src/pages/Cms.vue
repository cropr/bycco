<template>
  <v-app>
    <sidebar />
    <topbar />
    <v-parallax  v-if="landing && $vuetify.breakpoint.mdAndUp"
                 src="/static/img/pier_big.jpg" height="400" />
    <v-parallax v-if="landing && $vuetify.breakpoint.sm"
                src="/static/img/pier_medium.jpg" height="300" />
    <v-parallax v-if="landing && $vuetify.breakpoint.xs"
                src="/static/img/pier_small.jpg" height="200" />
    <v-content :class="{landing: landing}">
      <v-container>
        <div class="mainarea my-1">
          <cms-content class="pa-1" />
        </div>
      </v-container>
      <v-parallax  v-if="landing && $vuetify.breakpoint.mdAndUp"
                   src="/static/img/bekers_big.jpg" height="400" />
      <v-parallax v-if="landing && $vuetify.breakpoint.sm"
                  src="/static/img/bekers_medium.jpg" height="300" />
      <v-parallax v-if="landing && $vuetify.breakpoint.xs"
                  src="/static/img/bekers_small.jpg" height="200" />

      <v-container v-if="landing" class="mt-3 mb-2">
        <h2>{{ $t('News items')}}</h2>

        <!-- <cms-newsitems /> -->
      </v-container>
      <v-parallax  v-if="landing && $vuetify.breakpoint.smAndUp"
                   src="/static/img/winnaars_big.jpg" height="400" />
      <v-parallax v-if="landing && $vuetify.breakpoint.xs"
                  src="/static/img/winnaars_small.jpg" height="200" />

    </v-content>

    <ad-carousel class="mt-4 mb-3"/>
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
    sidebar: window.config.sidebar,

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

<style>
.landing.v-content {
  padding-top: 0px !important;
}
.img-responsive {
  max-width: 100%;
}
</style>