<template>
<div>
<h1>Attendees New version</h1>
<v-tabs v-model="tabix" class="blue-grey lighten-3" light slider-color="pink">
  <v-tab>Attendees</v-tab>
  <v-tab>Detail</v-tab>
  <v-tab>Photo</v-tab>
  <v-tab>Badge</v-tab>
  <v-tab>Name Card</v-tab>
</v-tabs>

<v-tabs-items v-model="tabix">
  <v-tab-item>
    <h3 class="mt-2">Attendee</h3>
    <p>To DO</p>
  </v-tab-item>
  <v-tab-item>
    <h3 class="mt-2">Detail</h3>
    <p>To DO</p>
  </v-tab-item>
  <v-tab-item>
    <h3 class="mt-2">Photo</h3>
    <p>To DO</p>
  </v-tab-item>
  <v-tab-item>
    <mg-attendee-badge></mg-attendee-badge>
  </v-tab-item>
  <v-tab-item>
    <mg-attendee-namecard></mg-attendee-namecard>
  </v-tab-item>
</v-tabs-items>
</div>
</template>

<script>
import _ from 'lodash';
import api from '../api/api';
import MgAttendeeNameCard from './MgAttendeeNameCard';
import MgAttendeeBadge from './MgAttendeeBadge';

export default {
  components: {
    "mg-attendee-badge": MgAttendeeBadge,
    "mg-attendee-namecard": MgAttendeeNameCard,
  },
  data () {
    return {
      tabix: "0"
    }
  },
  methods: {
  }
}
</script>

<style>
</style>
