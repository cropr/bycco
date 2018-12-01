<template>
<div>

<h1>SWAR management</h1>

<v-tabs class="blue-grey lighten-3" light slider-color="pink" v-model="tabix">
  <v-tab class="mx-2">
    Overview
  </v-tab>
  <v-tab class="mx-2">
    <span v-text="currentSwartrn.shortname"></span>
  </v-tab>
</v-tabs>
<v-tabs-items v-model="tabix">
  <v-tab-item>
    <mg-swar-overview :swartrns="swartrns" @openSwar="openSwar"></mg-swar-overview>
  </v-tab-item>
  <v-tab-item>
    <mg-swar-detail :swartrn="currentSwartrn" :tabix="tabix"></mg-swar-detail>
  </v-tab-item>
</v-tabs-items>

</div>

</template>

<script>
import api from '../api/api';
import MgSwarOverview from './MgSwarOverview';
import MgSwarDetail from './MgSwarDetail';

export default {
  components: {
    "mg-swar-overview": MgSwarOverview,
    "mg-swar-detail": MgSwarDetail,

  },
  data () {
    return {
      trns: [],
      swartrns: [],
      tabix: "0",
      currentSwartrn: {},
    }
  },
  methods: {
    getSwartrns () {
      var self = this;
      api('getSwarTournaments').then(
        function (data) {
          self.swartrns = data.swartrns || [];
        },
        function (data) {
          console.error('gettings swartrn failed', data)
        }
      )
    },
    openSwar (st) {
      console.log('opening swar', st.shortname);
      this.currentSwartrn = st;
      this.tabix = "1";
    },
  },
  mounted () {
    this.getSwartrns();
  },
}
</script>

<style>
</style>
