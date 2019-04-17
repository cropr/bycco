<template>
<div class="mt-2">
  <div v-show="standings.length && round<=topround">
    <v-data-table :items="standings" class="elevation-1" :headers="headers"  
                  hide-actions>
      <template slot="items" slot-scope="props">
        <td >{{ props.index + 1 }}</td>
        <td >{{ props.item.name }}</td>
        <td >{{ props.item.points }}</td>
        <td >{{ props.item.ngames }}</td>
        <td >{{ props.item.gender }}</td>
        <td >{{ props.item.rating }}</td>
        <td >{{ props.item.id_club }}</td>
        <td class="hidden-xs-only">{{ props.item.tpr }}</td>
        <td class="hidden-xs-only">{{ props.item.tiebreak[0].Points }}</td>
        <td class="hidden-xs-only">{{ props.item.tiebreak[1].Points }}</td>
        <td class="hidden-xs-only">{{ props.item.tiebreak[2].Points }}</td>
        <td class="hidden-xs-only">{{ props.item.tiebreak[3].Points }}</td>
        <td class="hidden-xs-only">{{ props.item.tiebreak[4].Points }}</td>
      </template>
    </v-data-table>
  </div>

  <div class="elevation-1 my-2 mx-1 pa-2" v-show="!standings.length || round>topround">
    {{$t("No standings available yet")}}  
  </div>
</div>
</template>

<script>

import api from '../util/api';

export default {

  props: ['updateTrn'],
  
  computed: {
    headers () { return [
      {
        text: "N",
        sortable: false,
        align: 'center',
        value: ''
      },
      {
        text: this.$t('Name'),
        sortable: false,
        align: 'left',
        value: 'name'
      },
      {
        text: this.$t('Points'),
        sortable: false,
        align: 'right',
        value: 'points'
      },
      {
        text: this.$t('Games'),
        sortable: false,
        align: 'right',
        value: 'ngames'
      },      {
        text: this.$t('Gender'),
        sortable: false,
        align: 'center',
        value: 'gender'
      },
      {
        text: 'Rating',
        sortable: false,
        align: 'right',
        value: 'rating'
      },
      {
        text: 'Club',
        sortable: false,
        align: 'center',
        value: 'id_club'
      },
      {
        text: 'TPR',
        sortable: false,
        align: 'right',
        value: 'tpr'
      },
      {
        text: 'TB1',
        sortable: false,
        align: 'right',
        value: 'tiebreak[0].Points'
      },
      {
        text: 'TB2',
        sortable: false,
        align: 'right',
        value: 'tiebreak[1].Points'
      },
      {
        text: 'TB3',
        sortable: false,
        align: 'right',
        value: 'tiebreak[2].Points'
      },
      {
        text: 'TB4',
        sortable: false,
        align: 'right',
        value: 'tiebreak[0].Points'
      },
      {
        text: 'TB5',
        sortable: false,
        align: 'right',
        value: 'tiebreak[0].Points'
      },
    ]},
  },
  
  data () {
    return {
      trn: {},
      standings: [
        // {name: 'ikke', points: '1.0', gender: 'M', rating: 1534},
        // {name: 'jij', points: '1.0', gender: 'F', rating: 1432},        
      ],
      round: 1,
      topround: 1,
    }
  },
  methods: {
    getStandings () {
      this.standings = [];
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
      api('getStandings', {
        id_trn: this.trn.id,
        round: this.round
      }).then(
        function(data){
          this.standings = data.standings;
        }.bind(this),
        function(data) {
          console.error('failed getting standings', data);
        }
      );
    }
  },
  watch: {
    updateTrn: function(newVal) {
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
