<template>
<div class="mt-2">
  <div v-show="pairings.length && round<=topround">
    <v-data-table :items="pairings" class="elevation-1" :headers="headers"  
                  hide-actions>
      <template slot="items" slot-scope="props">
        <td >{{ props.index + 1 }}</td>
        <td >{{ props.item.white }}</td>
        <td >{{ props.item.result }}</td>
        <td >{{ props.item.black }}</td>
      </template>
    </v-data-table>
  </div> 

  <div class="elevation-1 my-2 mx-1 pa-2"  v-show="!pairings.length || round>topround">
      {{$t("No pairings available yet")}}
  </div>
</div>
</template>

<script>

import api from '../util/api';

export default {

  name: 'TrnViewPairings',

  props: ['updateTrn'],
  
  computed: {

    headers () { return [
      {
        text: "N",
        sortable: false,
        align: 'left',
      },
      {
        text: this.$t('White'),
        sortable: false,
        align: 'left',
        value: 'white'
      },
      {
        text: "",
        sortable: false,
        align: 'center',
        value: 'result'
      },
      {
        text: this.$t('Black'),
        sortable: false,
        align: 'center',
        value: 'black'
      },
    ]},

  },

  data () {
    return {
      trn: {},
      pairings: [
        // {white: 'ikke', result: ' - ', black: 'me'},
        // {white: 'jij', result: ' - ', black: 'je'},
      ],
      round: 1,
      topround: 1,
    }
  },
  
  methods: {
  
    getPairings () {
      console.log('getPairings', this.trn);
      this.pairings = [];
      api('getTopround', {
        id_trn: this.trn.id,
      }).then(
        function(data){
          this.topround = data;
        }.bind(this),
        function(data) {
          console.error('failed getting topround', data);
        }
      );
      api('getPairings', {
        id_trn: this.trn.id,
        round: this.round
      }).then(
        function(data){
          this.pairings = data.pairings;
        }.bind(this),
        function(data) {
          console.error('failed getting pairings', data);
        }
      )
    }

  },
  
  watch: {
    updateTrn: function(newVal) {
      console.log('updateTrn watcher', newVal)
      this.trn = newVal.trn;
      this.round = newVal.round;
      this.getPairings();
    },
  }
}
</script>

<style>
</style>
