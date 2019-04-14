<template>
<v-app>
  <sidebar />
  <topbar />
  <v-content class="viewcontent">
    <v-tabs light slider-color="pink" v-model="tabix">
      <v-tab class="mx-2">
        <span>{{$t("Organizers")}}</span>
      </v-tab>
      <v-tab class="mx-2">
        <span>{{$t("Arbiters")}}</span>
      </v-tab>
    </v-tabs>
    <v-tabs-items v-model="tabix">
      <v-tab-item>
        <v-layout row wrap>
          <person :photourl="https:/api/subscriptions/420/photo"  
            :fullname="Ruben Decrop"
            :mobile="+32477571313" :email="ruben@decrop.net" /> 
        </v-layout>
      </v-tab-item>
      <v-tab-item>
      </v-tab-item>
    </v-tabs-items>
  </v-content>
  <ad-carousel />
  <bycco-footer />
</v-app>
 
</template>

<script>
import { loadLanguageAsync } from '../util/lang'
// import { mapState } from 'vuex'
import api from '../util/api'

import Sidebar from '../components/Sidebar'
import Topbar from '../components/Topbar'
import AdCarousel from '../components/AdCarousel'
import ByccoFooter from '../components/ByccoFooter'
import Person from '../components/Person'


const catmapping = {
  G8: 'U8',
  B8: 'U8',
  G10: 'G10',
  B10: 'B10',
  G12: 'G12',
  B12: 'B12',
  G14: 'G14',
  B14: 'B14',
  G16: 'G16',
  B16: 'B16',
  G18: 'G18',
  B18: 'B18',
  G20: 'U20',
  B20: 'U20',
  IMT: 'IMT',
};

export default {

  components: {
    Sidebar,
    Topbar,
    ByccoFooter,
    AdCarousel,
    Person,
  },

data () {
    return {

    }
  },

  methods: {


  },

  mounted () {

  },

  created () {
    loadLanguageAsync(window.config.lang);
  },
}
</script>
<style scoped>

</style>
