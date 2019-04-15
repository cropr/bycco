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
          <person :idsub="p.id" v-for="p in organizers" :key="p.id"/> 
        </v-layout>
      </v-tab-item>
      <v-tab-item>
        <v-layout row wrap>
          <person :idsub="p.id" v-for="p in arbiters" :key="p.id"/> 
        </v-layout>
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
      tabix: 0,
      organizers: [],
      arbiters: [],
    }
  },

  methods: {
    getAttendees () {
      api('getAttendees', {
        cat: 'ARB,ORG'
      }).then(
        function(data){
          this.organizers = [];
          this.arbiters = [];
          console.log('attendees', data.attendees)
          data.attendees.forEach(function(p){
            if (p.category == 'ORG') this.organizers.push(p);
            if (p.category == 'ARB') this.arbiters.push(p);
          }.bind(this))
        }.bind(this),
        function(data){
          console.log('error getting orgarb', data);
        }
      );
    }


  },

  mounted () {
    this.getAttendees()
  },

  created () {
    loadLanguageAsync(window.config.lang);
  },
}
</script>
<style scoped>

</style>
