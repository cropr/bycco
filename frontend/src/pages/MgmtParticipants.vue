<template>
<v-container fluid>

<h1>Management Participants</h1>

<v-tabs v-model="tabix" class="blue-grey lighten-3" light slider-color="pink">
  <v-tab>Participants</v-tab>
  <v-tab>Detail</v-tab>
  <v-tab>Photo</v-tab>
  <v-tab>Invoice</v-tab>
  <v-tab>Badges</v-tab>
  <v-tab>Name Cards</v-tab>
</v-tabs>

<v-tabs-items v-model="tabix">
  <v-tab-item>
    <mgmt-part-list />
  </v-tab-item>
  <v-tab-item>
    <h3 class="mt-2">Details</h3>
    <p>To DO</p>
  </v-tab-item>
  <v-tab-item>
    <h3 class="mt-2">Photo</h3>
    <p>To DO</p>
  </v-tab-item>
  <v-tab-item>
    <h3 class="mt-2">Invoice</h3>
    <p>To DO</p>
  </v-tab-item>
  <v-tab-item>
    <!--<mg-attendee-badge></mg-attendee-badge>-->
  </v-tab-item>
  <v-tab-item>
    <!--<mg-attendee-namecard></mg-attendee-namecard>-->
  </v-tab-item>
</v-tabs-items>

</v-container>
</template>

<script>

import MgmtPartList  from '../components/MgmtPartList'

export default {
  name: "MgmtParticipants",

  data () {return {
    tabix: 0,
  }},

  components: {
    MgmtPartList,
  }
}
</script>

<style scoped>

</style>