<template>
<div>
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
    <mgmt-trns-overview :trns="trns" @openTrn="openTrn" @updateTrns="gettrns" />
  </v-tab-item>
  <v-tab-item>
    <mgmt-trns-detail :trn="currentTrn" :tabix="tabix" />
  </v-tab-item>
</v-tabs-items>

</div>

</template>

<script>
import api from '../util/api';
import MgmtTrnsOverview from '../components/MgmtTrnsOverview';
import MgmtTrnsDetail from '../components/MgmtTrnsDetail';

export default {

  name: 'MgmgTrns',

  components: {
    MgmtTrnsOverview,
    MgmtTrnsDetail,
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
      api('getTournaments').then(
        function (data) {
          this.trns = data.trns;
        }.bind(this),
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
