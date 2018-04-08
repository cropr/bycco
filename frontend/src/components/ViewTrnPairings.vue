<template>
<div class="mt-2">

  <v-card class="ma-2" v-show="pairings.length">
    <v-card-title>
      <h4>Pairings Round <span v-text="round"></span></h4>
    </v-card-title>
    <v-card-text>
      <table style="width:auto;">
        <tr v-for="(p,ix) in pairings" :key="p.white">
          <td class="px-2" v-text="ix + 1"></td>
          <td class="px-2" v-text="p.white"></td>
          <td class="px-2" v-text="p.result"></td>
          <td class="px-2" v-text="p.black"></td>
        </tr>
      </table>
    </v-card-text>
  </v-card>
  <v-card class="ma-2" v-show="!pairings.length">
    <v-card-title>
      <h4>Pairings</h4>
    </v-card-title>
    <v-card-text>
      No pairings available yet
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
      pairings: [],
      round: 1,
    }
  },
  methods: {
    getPairings () {
      var self=this;
      api('getPairings', {
        id_trn: this.trn.id,
        round: this.round
      }).then(
        function(data){
          self.pairings = data.pairings;
        },
        function(data) {
          console.error('failed getting pairings', data);
        }
      )
    }
  },
  watch: {
    updateTrn: function(newVal, oldVal) {
      console.log('new Value for Trn', newVal);
      this.trn = newVal.trn;
      this.round = newVal.round;
      this.getPairings();
    },
  }
}
</script>

<style>
</style>
