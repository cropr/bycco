<template>
<div class="mt-2">
  <v-card class="ma-2" v-show="standings.length && round<=topround">
    <v-card-title>
      <h4>Standings Round <span v-text="round"></span></h4>
    </v-card-title>
    <v-card-text>
      <table style="width:auto;" v-show="standings.length">
        <tr>
          <th>N.</th>
          <th class="px-1">Name</th>
          <th class="px-1">Points</th>
          <th class="px-1">Games</th>
          <th class="px-1">Gender</th>
          <th class="px-1 hidden-xs-only">Rating</th>
          <th class="px-1 hidden-xs-only">TB1</th>
          <th class="px-1 hidden-xs-only">TB2</th>
          <th class="px-1 hidden-xs-only">TB3</th>
          <th class="px-1 hidden-xs-only">TB4</th>
          <th class="px-1 hidden-xs-only">TB5</th>
        </tr>
        <tr v-for="(s,ix) in standings" :key="s.id">
          <td class="px-2" v-text="ix+1"></td>
          <td class="px-2" v-text="s.name"></td>
          <td class="px-2" v-text="s.points"></td>
          <td class="px-2" v-text="s.ngames"></td>
          <td class="px-2" v-text="s.gender"></td>
          <td class="px-2 hidden-xs-only" v-text="s.rating"></td>
          <td class="px-2 hidden-xs-only" v-text="s.tiebreak[0].Points"></td>
          <td class="px-2 hidden-xs-only" v-text="s.tiebreak[1].Points"></td>
          <td class="px-2 hidden-xs-only" v-text="s.tiebreak[2].Points"></td>
          <td class="px-2 hidden-xs-only" v-text="s.tiebreak[3].Points"></td>
          <td class="px-2 hidden-xs-only" v-text="s.tiebreak[4].Points"></td>
        </tr>
      </table>
    </v-card-text>
  </v-card>
  <v-card class="ma-2" v-show="!standings.length || round>topround">
    <v-card-title>
      <h4>Standings</h4>
    </v-card-title>
    <v-card-text>
      No standings available yet
    </v-card-text>
  </v-card>
</div>
</template>

<script>

import api from '../api/api';

export default {
  props: ['updateTrn'],
  data () {
    return {
      trn: {},
      standings: [],
      round: 1,
      topround: 1,
    }
  },
  methods: {
    getStandings () {
      var self=this;
      api('getTopround', {
        id_trn: this.trn.id,
      }).then(
        function(data){
          self.topround = data;
        },
        function(data) {
          console.error('failed getting topround', data);
        }
      );
      api('getStandings', {
        id_trn: this.trn.id,
        round: this.round
      }).then(
        function(data){
          self.standings = data.standings;
        },
        function(data) {
          console.error('failed getting standings', data);
        }
      );
    }
  },
  watch: {
    updateTrn: function(newVal, oldVal) {
      console.log('new Value for Trn', newVal);
      this.trn = newVal.trn;
      this.round = newVal.round;
      this.getStandings();
    },
  }
}
</script>

<style>
</style>
