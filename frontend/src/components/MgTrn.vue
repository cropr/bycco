<template>
<div>

<h1>Tournaments</h1>

<v-tabs v-model="tabix" class="blue-grey lighten-3" light
    slider-color="pink">
  <v-tab class="mx-2">
    Overview
  </v-tab>
  <v-tab class="mx-2">
    <span v-text="currentTrn.shortname"></span>
  </v-tab>
</v-tabs>

<v-tabs-items v-model="tabix">
  <v-tab-item>
    <mg-trn-overview :trns="trns" @openTrn="openTrn" @updateTrns="getttrns"></mg-trn-overview>
  </v-tab-item>
  <v-tab-item>
    <mg-trn-detail :trn="currentTrn"></mg-trn-detail>
  </v-tab-item>
</v-tabs-items>

</div>

</template>

<script>
import api from '../api/api';
import MgTrnOverview from './MgTrnOverview';
import MgtrnDetail from './MgTrnDetail';

export default {
  components: {
    "mg-trn-overview": MgTrnOverview,
    "mg-trn-detail": MgtrnDetail,
  },
  data () {
    return {
      trns: [],
      tabix: 0,
      currentTrn: {},
    }
  },
  methods: {
    gettrns () {
      var self = this;
      api('getTournaments').then(
        function (data) {
          self.trns = data.trns;
        },
        function (data) {
          console.error('adding trn failed', data)
        }
      )
    },
    openTrn (t) {
      console.log('opening trn', t);
      this.currentTrn = t;
      this.tabix = 1;
    }
  },
  mounted () {
    this.gettrns();
  },
}
</script>

<style>
</style>
