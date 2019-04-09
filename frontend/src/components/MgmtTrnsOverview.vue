<template>
<div >
  <v-layout>
    <v-flex xs12 sm6>
      <v-card class="mt-2 mb-2 ml-2 mr-2" light>
        <v-card-title class="blue-grey lighten-4 headline">
          Add a new tournament
        </v-card-title>
        <v-card-text>
          <v-text-field label="Full name tournament" v-model="name">
          </v-text-field>
          <v-text-field label="Short name tournament" v-model="shortname">
          </v-text-field>
          <v-text-field label="Number of rounds" type="number" v-model="rounds">
          </v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-btn @click="addtrn" class="blue-grey" color="primary">
            Add Tournament
          </v-btn>
        </v-card-actions>
      </v-card>

    </v-flex>
  </v-layout>

  <v-layout>
    <v-flex xs12 sm6>
      <v-card class="mt-2 mb-2 ml-2 mr-2">
        <v-card-title class="blue-grey lighten-4 headline">
          Existing tournaments
        </v-card-title>
        <v-card-text>
          <v-layout v-for="(t,ix) in trns" :key="t.shortname" class="my-1">
            <v-flex xs1 v-text="ix+1"></v-flex>
            <v-flex xs11>
              <a href="#" @click="opentrn(t)" v-text="t.name"></a>
            </v-flex>
          </v-layout>
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>

</div>
</template>

<script>

import api from '../util/api';

export default {

  name: 'MgmtTrnsOverview',

  props: ['trns'],
  
  data () {
    return {
      name: '',
      shortname: '',
      rounds: 9
    }
  },

  methods: {
  
    addtrn () {
      api('addTournament', {
        name: this.name,
        shortname: this.shortname,
        rounds: this.rounds
      }).then(
        function(){
          this.$emit('updateTrns')
        }.bind(this),
        function(data) {
          console.error('adding trn failed', data)
        }
      )
    },

    opentrn (t) {
      console.log('opening trn', t);
      this.$emit('openTrn', t);
    },

  },

}
</script>

<style>
</style>
