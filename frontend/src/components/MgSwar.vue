<template>
<div>

<h1>Tournaments</h1>

<v-tabs v-model="tabix" class="blue-grey lighten-3" light
    slider-color="pink">
  <v-tab @click="gotoTab('overview')" class="mx-2">
    Overview
  </v-tab>
  <v-tab @click="gotoTab('existing')" class="mx-2">
    <span v-text="currentTrn.shortname"></span>
  </v-tab>
</v-tabs>

<v-tabs-items v-model="tabix">
  <v-tab-item>
    <mg-trn-overview :trns="trns" @openTrn="openTrn"></mg-trn-overview>
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
import MgTrnDetail from './MgTrnDetail';

export default {
  components: {
    "mg-trn-overview": MgTrnOverview,
    "mg-trn-detail": MgTrnDetail,
  },
  data () {
    return {
      trns: [],
      tabix: 0,
      currentTrn: {},
    }
  },
  methods: {
    gotoTab (tabname) {

    },
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
    // updating () {
    //   let cats = [], self=this;
    //   _.forEach(this.cat, function(v, k){
    //     if (v) {
    //       cats.push(...v.split(','));
    //     }
    //   });
    //   api('getAttendees', {
    //     count: 999,
    //     cat: cats.join(',')
    //   }).then(function(data){
    //     console.log('data', data);
    //     self.attendees = [];
    //     data.attendees.forEach(function(p){
    //       if (p.confirmed) {
    //         self.attendees.push(p)
    //       };
    //     });
    //   self.sortAttendees();
    //   }, function(data){
    //     console.log('error getting attendees', data);
    //   });
    // },
    // sortAttendees () {
    //   console.log('sorting');
    //   this.attendees.sort(function(a,b){
    //     if (a.present < b.present) return -1;
    //     if (a.present > b.present) return 1;
    //     if (a.lastname < b.lastname) return -1;
    //     if (a.lastname > b.lastname) return 1;
    //     if (a.firstname < b.firstname) return -1;
    //     if (a.firstname > b.firstname) return 1;
    //     return 0;
    //   })
    // }
  },
  mounted () {
    this.gettrns();
  },
}
</script>

<style>
</style>
