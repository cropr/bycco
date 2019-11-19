<template>

<v-app>

  <mgmt-sidebar />

  <mgmt-topbar />

  <router-view></router-view>
  
  <mgmt-footer />

</v-app>

</template>

<script>
import {mapState} from "vuex"

import Sidebar from '../components/Sidebar.vue'
import Topbar from '../components/Topbar.vue'
import ByccoFooter from '../components/ByccoFooter.vue'
import AdCarousel from '../components/AdCarousel.vue'

export default {

  name: 'LandingsPage',

  data () {return {
    articles: [
      {id:1, title: "Article 1", intro: "Some bullshit"},
      {id:2, title: "Article 2", intro: "Some more bullshit"},
      {id:3, title: "Article 3", intro: 
        "Some very long bullshit, that needs some wrapping"},
      {id:4, title: "Article 4", intro: "Some bullshit with <b>bold</b> in it"},
    ]
  }},

  components: {
    Sidebar,
    Topbar,
    ByccoFooter,
    AdCarousel,
  },

  computed: {
    ...mapState(['page', 'slug', 'lang'])
  },

}
</script>


<style scoped>

.nopadding {
  padding-top: 0px !important;
}
/* .img-responsive {
  max-width: 100%;
} */
</style>
