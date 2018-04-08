<template>

<v-container>
  <h3 class="mt-2">Badge</h3>
  <v-layout>
    <v-flex xs6>
      <v-text-field placeholder="Search last name" v-model="ss"
                    append-icon="search"></v-text-field>
    </v-flex>
    <v-flex xs6>
      <v-btn color="primary" @click="search">Search</v-btn>
      <v-btn color="primary" @click="printBadges">Print</v-btn>
    </v-flex>
  </v-layout>

  <v-card>
    <v-card-title>
      <h4 class="mt-2">Found players</h4>
    </v-card-title>
    <v-card-text>
      <v-layout v-for="(p,ix) in attendees" :key="p.id" v-show="!p.selected">
        <v-flex xs1>
          <v-checkbox @change="selectAttendee(p)" v-model="p.selected"></v-checkbox>
        </v-flex>
        <v-flex xs4>
          <span v-text="p.first_name"></span>
          <span v-text="p.last_name"></span>
          <span v-text="p.category"></span>
        </v-flex>
      </v-layout>
    </v-card-text>
  </v-card>

  <v-card>
    <v-card-title>
      <h4 class="mt-2">Selected attendees</h4>
    </v-card-title>
    <v-card-text>
      <v-layout v-for="(p,ix) in selected" :key="p.id">
        <v-flex xs4>
          <span v-text="p.first_name"></span>
          <span v-text="p.last_name"></span>
          <span v-text="p.category"></span>
        </v-flex>
        <v-flex xs2>
          <v-btn @click="remove(p)">Delete</v-btn>
        </v-flex>
      </v-layout>
    </v-card-text>
  </v-card>v

</v-container>

</template>

<script>
import _ from 'lodash';
import api from '../api/api';

export default {
  data () {
    return {
      tabix: "0",
      attendees: [],
      ss: '',
      selected: [],
    }
  },
  methods: {
    printBadges () {
      console.log('should print');
      var ids = [];
      _.forEach(this.selected, function(pl){
        ids.push(pl.id)
      });
      location.href = '/subscribe/printbadges?ids=' + ids.join(',')
    },
    remove (pl) {
      _.remove(this.selected, function(n) {return n.id == pl.id});
      var a = _.find(this.attendees, function(n) {return n.id == pl.id});
      if (a) {
        a.selected = false;
      }
    },
    search () {
      var self=this;
      api('getAttendees', {
        start: 0,
        count: 999,
        ss: this.ss,
        cat: null,
      }).then(
        function(data){
          self.attendees = [];
          _.forEach(data.attendees, function(pl){
            pl.selected = false;
            self.attendees.push(pl);
          });
        },
        function(data){
          console.error('Error gettting attendees', data);
        }
      );
    },
    selectAttendee (pl) {
      this.selected.push(pl);
      pl.selected = true;
    }
  }
}
</script>

<style>
</style>
