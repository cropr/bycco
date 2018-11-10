<template>
<div >
<h1>Presence Check</h1>
<v-container>
  <h3>Categories</h3>

  <v-layout row wrap>
    <v-flex md1 sm2 xs3>
      <v-checkbox :label="'BG8'" :value="'B8,G8'" v-model="cat.bg8" @change="updating"></v-checkbox>
    </v-flex>
    <v-flex md1 sm2 xs3>
      <v-checkbox :label="'BG10'" :value="'B10,G10'" v-model="cat.bg10" @change="updating"></v-checkbox>
    </v-flex>
    <v-flex md1 sm2 xs3>
      <v-checkbox  :label="'BG12'" :value="'B12,G12'" v-model="cat.bg12" @change="updating"></v-checkbox>
    </v-flex>
    <v-flex md1 sm2 xs3>
      <v-checkbox :label="'BG14'" :value="'B14,G14'" v-model="cat.bg14" @change="updating"></v-checkbox>
    </v-flex>
    <v-flex md1 sm2 xs3>
      <v-checkbox :label="'BG16'" :value="'B16,G16'" v-model="cat.bg16" @change="updating"></v-checkbox>
    </v-flex>
    <v-flex md1 sm2 xs3>
      <v-checkbox :label="'BG18'" :value="'B18,G18'" v-model="cat.bg18" @change="updating"></v-checkbox>
    </v-flex>
    <v-flex md1 sm2 xs3>
      <v-checkbox :label="'BG20'" :value="'B20,G20'" v-model="cat.bg20" @change="updating"></v-checkbox>
    </v-flex>
    <v-flex md1 sm2 xs3>
      <v-checkbox :label="'EAT'" :value="'EAT'" v-model="cat.eat" @change="updating"></v-checkbox>
    </v-flex>
    <v-flex md1 sm2 xs3>
      <v-checkbox :label="'ORG'" :value="'ORG,ARB'" v-model="cat.org" @change="updating"></v-checkbox>
    </v-flex>
  </v-layout>
  <h3>Attendees</h3>
  <mg-presence-attendee v-for="(p, ix) in attendees" :key="p.id"
                        :attendee="p" :ix="ix" @doUpdate="updating">
  </mg-presence-attendee>

</v-container>

</div>
</template>

<script>
import _ from 'lodash';
import api from '../api/api';
import MgPresenceAttendee from "./MgPresenceAttendee";

export default {
  components: {MgPresenceAttendee},
  data () {
    return {
      attendees : [],
      cat: {
        bg8: false,
        bg10: false,
        bg12: false,
        bg14: false,
        bg16: false,
        bg18: false,
        bg20: false,
        eat: false,
        org: false,
        arb: false,
      }
    }
  },
  methods: {
    updating () {
      let cats = [], self=this;
      _.forEach(this.cat, function(v, k){
        if (v) {
          cats.push(...v.split(','));
        }
      });
      console.log('cats', cats);
      api('getAttendees', {
        count: 999,
        cat: cats.join(',')
      }).then(function(data){
        console.log('data', data);
        self.attendees = [];
        data.attendees.forEach(function(p){
          self.attendees.push(p)
        });
      self.sortAttendees();
      }, function(data){
        console.log('error getting attendees', data);
      });
    },
    sortAttendees () {
      console.log('sorting');
      this.attendees.sort(function(a,b){
        if (a.present < b.present) return -1;
        if (a.present > b.present) return 1;
        if (a.lastname < b.lastname) return -1;
        if (a.lastname > b.lastname) return 1;
        if (a.firstname < b.firstname) return -1;
        if (a.firstname > b.firstname) return 1;
        return 0;
      })
    }
  }
}
</script>

<style>
</style>
