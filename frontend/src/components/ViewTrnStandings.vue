<template>
<v-card class="ma-1">
  <v-card-title>Pairings Round<span v-text="currentRound"></span> </v-card-title>
    <table class="table" style="width:auto;" ng-show="pairings.length">
      <tr>
        <th>N.</th>
        <th>White</th>
        <th>Result</th>
        <th>Black</th>
      </tr>
      <tr v-for="(p,ix) in pairings" :key="p.white">
        <td v-text="p.black ? ix+1 : ''"></td>
        <td>
          <span v-text="p.white"></span>
          <span class="hidden-xs">
            (<span v-text="p.white_rating"></span> :
            <span v-text="p.white_points.toFixed(1)"></span>)
          </span>
        </td>
        <td>
          <span v-text="result(p)"></span>
        </td>
        <td>
          <span v-text="p.black"></span>
          <span class="hidden-xs" v-show="p.black">
            (<span v-text="p.black_rating"></span> :
            <span v-text="p.black_points.toFixed(1)"></span>)
          </span>
        </td>
      </tr>
    </table>
    <div ng-hide="pairings.length">
      No pairings available
    </div>
</v-card>
</template>

<script>
import _ from 'lodash';
import api from '../api/api';

export default {
  props: ['trn'],
  data () {
    return {
      currentRound: 1,
    }
  },
  methods: {
  },
}
</script>

<style>
</style>
