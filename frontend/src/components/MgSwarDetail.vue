<template>
<v-layout>
  <v-flex xs12 sm6>
    <v-card class="mt-2 mb-2 ml-2 mr-2" light>
        <v-card-title class="blue-grey lighten-4 headline"
                      v-text="trn.name">
        </v-card-title>
        <v-card-text>
          <span v-text="prizes.length" v-show="prizes.length"></span>
          <span v-show="prizes.length">prizes available</span>
          <span v-show="!prizes.length">
            No prizes generated
          </span>
        </v-card-text>
        <v-card-actions>
          <v-btn class="blue-grey" color="primary" @click="generatePrizes">
            Generate Prizes
          </v-btn>
          <v-btn class="blue-grey" color="primary" @click="printPrizes">
            Print Prizes
          </v-btn>
        </v-card-actions>
    </v-card>
  </v-flex>
</v-layout>
</template>

<script>
import api from '../api/api';

export default {
  props: ['trn'],
  data () {
    return {
      prizes: []
    }
  },
  methods: {
    generatePrizes () {
      console.log('generatePrizes')
    },
    printPrizes () {
      console.log('printPrizes')
    },
  }
}
</script>

<style>
</style>
