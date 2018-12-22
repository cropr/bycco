<template>
<v-container fluid grid-list-md class="elevation-1">

  <v-layout row wrap>
    <v-flex sm6 xs12>
      <v-text-field append-icon="search" @click:append="search" v-model="ss" />
    </v-flex>
    <v-flex sm4 xs8>
      <v-select :items="catitems" v-model="catselected"></v-select>
    </v-flex>
    <v-flex sm2 xs4>
      <v-btn href="/trn/csv" >CSV</v-btn>
    </v-flex>
  </v-layout>

  <v-data-table :items="filteredParticipants" class="elevation-1" :headers="headers"
                :rows-per-page-items="[25,50,100]" :pagination.sync="pagination">
    <template slot="headers" slot-scope="props" >
      <tr>
        <th>
          <v-checkbox :input-value="props.all" :indeterminate="props.indeterminate"
            primary hide-details @click="toggleAll"
          ></v-checkbox>
        </th>
        <th v-for="header in props.headers" :key="header.text"
            :class="headerClasses(header)" @click="changeSort(header)">
          {{ header.text }}
          <v-icon small v-show="header.sortable">arrow_upward</v-icon>
        </th>
      </tr>
    </template>
    <template slot="items" slot-scope="props">
      <td>
        <v-checkbox :input-value="props.selected" primary hide-details></v-checkbox>
      </td>
      <td >{{ props.item.last_name }}</td>
      <td >{{ props.item.first_name }}</td>
      <td class="text-xs-center">{{ props.item.gender }}</td>
      <td class="text-xs-center">{{ props.item.category }}</td>
    </template>
  </v-data-table>

</v-container>
</template>

<script>

import api from '../util/api'
import _ from 'lodash'

export default {
  name: "MgmtPartList",

  computed: {
    filteredParticipants () {
      if (this.catselected == 'All')
        return this.participants;
      return _.filter(this.participants, function(p){
        return this.catsSelected[p.category]
      }.bind(this))
    },
    headers () { return [
      {
        text: 'Last name',
        align: 'left',
        sortable: true,
        value: 'last_name'
      },
      {
        text: 'First name',
        align: 'left',
        sortable: true,
        value: 'first_name'
      },
      {
        text: 'Gender',
        align: 'center',
        value: 'gender'
      },
      {
        text: 'Category',
        align: 'center',
        value: 'category'
      },
    ]},
  },


  data () {return {
    catitems: [
      {value: 'All', text: 'All'},
      {value: 'Players', text: 'Players Only'},
      {value: 'B8', text: 'B8'},
      {value: 'G8', text: 'G8'},
      {value: 'B10', text: 'B10'},
      {value: 'G10', text: 'G10'},
      {value: 'B12', text: 'B12'},
      {value: 'G12', text: 'G12'},
      {value: 'B14', text: 'B14'},
      {value: 'G14', text: 'G14'},
      {value: 'B16', text: 'B16'},
      {value: 'B16', text: 'B16'},
      {value: 'B16', text: 'B16'},
      {value: 'B16', text: 'B16'},
      {value: 'B16', text: 'B16'},
      {value: 'B16', text: 'B16'},
      {value: "ORG", text: 'Organiser'},
      {value: "ARB", text: 'Arbiter'},
      {value: "SPO", text: 'Sponsor or Guest'},
      {value: "EAT", text: 'Resident with meals'},
    ],
    catselected: 'All',
    pagination: {
      sortBy: 'last_name',
      descending: false,
    },
    participants: [],
    selected: [],
    ss: '',
  }},

  methods: {
    changeSort (header) {
      console.log('chnage sort', header.value, header.sortable)
      if (!header.sortable) return;
      if (this.pagination.sortBy === header.value) {
        this.pagination.descending = !this.pagination.descending
      } else {
        this.pagination.sortBy = header.value;
        this.pagination.descending = false
      }
    },
    headerClasses (header) {
      let hc = ['column'];
      hc.push(header.align ? 'text-xs-' + header.align : 'text-xs-left');
      hc.push(header.sortable ? 'sortable': '');
      hc.push(this.pagination.descending ? 'desc' : 'asc');
      hc.push(header.value === this.pagination.sortBy ? 'active' : '');
      return hc;
    },
    search () {
      console.log('searching')
    },
    toggleAll () {
      if (this.selected.length) {
        this.selected = []
      }
      else {
        this.selected = this.filteredParticipants.slice()
      }
    },
  },

  mounted () {
    api('getParticipants').then(
      function(data) {
        console.log('participants data', data);
        this.participants = data;
      }.bind(this)
    );
  },

}
</script>

<style scoped>

</style>