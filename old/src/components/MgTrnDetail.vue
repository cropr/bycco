<template>
<v-layout>
  <v-flex xs12 sm6>
    <v-card class="mt-2 mb-2 ml-2 mr-2" light>
        <v-card-title class="blue-grey lighten-4 headline"
                      v-text="trn.name">
        </v-card-title>
        <v-card-text>
          <div v-show="prizes.length">
            <span v-text="prizes.length"></span> prizes available.
          </div>
          <div v-show="!prizes.length">
            No prizes generated
          </div>
        </v-card-text>
        <v-card-actions>
          <v-btn class="blue-grey" color="primary" @click="createPrizes">
            Create Prizes
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
  props: ['trn', 'tabix'],
  data () {
    return {
      prizes: []
    }
  },
  methods: {
    createPrizes () {
      var self=this;
      self.prizes = [];
      api('createPrizes', {
        id_trn: this.trn.id
      }).then(
        function(data){
          console.log('created prizes', data);
          self.prizes = data.playerprizes
        },
        function(data) {
          console.error('Error creating prizes', data)
        }
      )
    },
    getPrizes () {
      var self=this;
      self.prizes = [];
      api('getPrizes', {
        id_trn: this.trn.id
      }).then(
        function(data){
          console.log('got prizes', data);
          self.prizes = data.playerprizes
        },
        function(data) {
          console.error('Error getting prizes', data)
        }
      )
    },
    printPrizes () {
      window.open('/subscribe/printprizes/' + this.trn.shortname)
    },
  },
  watch: {
    tabix: function(newVal, oldVal) {
      console.log('watch update', newVal);
      if (newVal == "1") {
        this.getPrizes();
      }
    }
  }
}
</script>

<style>
</style>
