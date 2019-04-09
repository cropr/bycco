<template>
<div>
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
      <mgmt-swar-overview :swartrns="swartrns" @openSwar="openSwar" />
    </v-tab-item>
    <v-tab-item>
      <mgmt-swar-detail :swartrn="currentSwartrn" :tabix="tabix" />
    </v-tab-item>
  </v-tabs-items>

</div>
</template>

<script>
import api from '../util/api';
import MgmtSwarFile from '../components/MgmtSwarFile';
import MgmtSwarOverview from '../components/MgmtSwarOverview';
import MgmtSwarDetail from '../components/MgmtSwarDetail';


export default {

  name: "MgmtSwar",

  components: {
    MgmtSwarFile,
    MgmtSwarDetail,
    MgmtSwarOverview,
  },

  data () {
    return {
      trns: [],
      swartrns: [],
      tabix: 0,
      currentSwartrn: {},
    }
  },

  methods: {
    getSwartrns () {
      api('getSwarTournaments').then(
        function (data) {
          this.swartrns = data.swartrns || [];
        }.bind(this),
        function (data) {
          console.error('gettings swartrn failed', data)
        }
      )
    },
    openSwar (st) {
      console.log('opening swar', st.shortname);
      this.currentSwartrn = st;
      this.tabix = 1;
    },
  },

  mounted () {
    this.getSwartrns();
  },

}
</script>

<style scoped>

</style>