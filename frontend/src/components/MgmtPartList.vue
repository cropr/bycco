<template>
<v-container fluid grid-list-md class="elevation-1">
  <v-layout row>
    <v-flex>
        <h1>Management Participants</h1>
    </v-flex>
    <v-flex>
      <v-tooltip bottom>
        <v-btn outline fab color="blue-grey" href="/trn/csv" slot="activator">
          <v-icon>cloud_download</v-icon>
        </v-btn>
        <span>CSV download</span>
      </v-tooltip>
      <v-tooltip bottom>
        <v-btn outline fab color="blue-grey" @click="gotoAdd()" slot="activator">
          <v-icon>add</v-icon>
        </v-btn>
        <span>New participant</span>
      </v-tooltip>
      <v-tooltip bottom>
        <v-btn outline fab color="blue-grey" @click="gotoBadge()" slot="activator">
          <v-icon>assignment_ind</v-icon>
        </v-btn>
        <span>Badge</span>
      </v-tooltip>
      <v-tooltip bottom>
        <v-btn outline fab color="blue-grey" @click="gotoNamecard()" slot="activator">
          <v-icon>assignment</v-icon>
        </v-btn>
        <span>Namecard</span>
      </v-tooltip>
      <v-tooltip bottom>
        <v-btn outline fab color="blue-grey" @click="gotoPresence()" slot="activator">
          <v-icon>check_box</v-icon>
        </v-btn>
        <span>Presence Check</span>
      </v-tooltip>
    </v-flex>
  </v-layout>

  <v-layout row wrap>
    <v-flex sm4 xs6>
      <v-text-field append-icon="search" @click:append="search" v-model="ss" />
    </v-flex>
    <v-flex sm4 xs6>
      <v-select :items="catitems" v-model="catselected" @change="changeCat()" />
    </v-flex>
    <v-flex>
      <v-checkbox label="Not confirmed" v-model="isNotConfirmed" />
    </v-flex>
  </v-layout>

  <v-data-table :items="filteredParticipants" class="elevation-1" :headers="headers"
                :rows-per-page-items="[25,50,100]" :pagination.sync="pagination">
    <template slot="headers" slot-scope="props" >
      <th v-for="header in props.headers" :key="header.text"
          :class="headerClasses(header)" @click="changeSort(header)">
        {{ header.text }}
        <v-icon small v-show="header.sortable">arrow_upward</v-icon>
      </th>
      <th class="text-xs-left">Actions</th>
    </template>
    <template slot="items" slot-scope="props">
      <td>{{ props.item.id }}</td>
      <td>{{ props.item.first_name }}</td>
      <td>{{ props.item.last_name }}</td>
      <td class="text-xs-center">{{ props.item.category }}</td>
      <td>
        <v-icon class="mr-1" @click="editParticipant(props.item)">edit</v-icon>
        <v-icon class="mr-1" @click="photoParticipant(props.item)">face</v-icon>
        <v-icon class="mr-1" @click="invoiceParticipant(props.item)">euro_symbol</v-icon>
        <v-icon class="mr-1" @click="printParticipant(props.item)">print</v-icon>
      </td>
    </template>
  </v-data-table>

</v-container>
</template>

<script>

import api from '../util/api'
import _ from 'lodash'

export default {
  name: "MgmtPartList",

  props: ['ts', 'selection'],

  computed: {
    filteredParticipants () {
      let result = this.participants,
          noplayers = ['All', 'Player', 'ORG', 'ARB', 'SPO', 'EAT'];
      if (this.catselected == 'Players')
         result =  _.filter(result, function(p) {
            return noplayers.indexOf(p.category) == -1;
         });
      if (this.isNotConfirmed)
        result = _.filter(result, ['confirmed', false]);
      // if (this.hasNoInvoice)
      //   retult = _.filter(result, ['invoiced', false])
      return result
    },
    headers () { return [
      {
        text: 'ID',
        align: 'left',
        sortable: true,
        value: 'id'
      },
      {
        text: 'First name',
        align: 'left',
        sortable: true,
        value: 'first_name'
      },
      {
        text: 'Last name',
        align: 'left',
        sortable: true,
        value: 'last_name'
      },
      {
        text: 'Category',
        align: 'center',
        value: 'category'
      },
    ]},
    catsearch () {
      if (['All', 'Players'].indexOf(this.catselected) >= 0 ) return null;
      return this.catselected;
    }

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
      {value: 'G16', text: 'G16'},
      {value: 'B18', text: 'B18'},
      {value: 'G18', text: 'G18'},
      {value: 'B20', text: 'B20'},
      {value: 'G20', text: 'G20'},
      {value: "IMT", text: 'IM toernooi'},
      {value: "ORG", text: 'Organiser'},
      {value: "ARB", text: 'Arbiter'},
      {value: "SPO", text: 'Sponsor or Guest'},
      {value: "EAT", text: 'Resident with meals'},
    ],
    catselected: 'All',
    catselectedOld: 'All',
    hasNoInvoice: false,
    isNotConfirmed: false,
    pagination: {
      sortBy: 'last_name',
      descending: false,
    },
    participants: [],
    selected: [],
    ss: '',
  }},

  methods: {
    changeCat () {
      if (this.catselected == 'All' || this.catselected == 'Players') {
        if (this.catselectedOld == 'All' || this.catselectedOld == 'Players'){
          // leave it as is, the filtering will do its job
        }
        else {
          this.getAttendees();
        }
      }
      else {
        this.getAttendees();
      }
      this.catselectedOld = this.catselected;
    },

    changeSort (header) {
      if (!header.sortable) return;
      if (this.pagination.sortBy === header.value) {
        this.pagination.descending = !this.pagination.descending
      } else {
        this.pagination.sortBy = header.value;
        this.pagination.descending = false
      }
    },

    editParticipant(p) {
      this.$emit('update', {
        section: 'edit',
        participant: p,
      })
    },

    getAttendees () {
      api('getAttendees', {
        cat: this.catsearch,
        ss: this.ss.length ? this.ss : null,
      }).then(
        function(data) {
          this.participants = data.attendees;
        }.bind(this)
      );
    },

    gotoAdd () {
      this.$emit('update', {section: 'add'})
    },

    gotoBadge () {
      this.$emit('update', {section: 'badge'})
    },

    gotoNamecard () {
      this.$emit('update', {section: 'namecard'})
    },

    gotoPresence () {
      this.$emit('update', {section: 'presence'})
    },

    headerClasses (header) {
      let hc = ['column'];
      hc.push(header.align ? 'text-xs-' + header.align : 'text-xs-left');
      hc.push(header.sortable ? 'sortable': '');
      hc.push(this.pagination.descending ? 'desc' : 'asc');
      hc.push(header.value === this.pagination.sortBy ? 'active' : '');
      return hc;
    },

    invoiceParticipant (p) {
      this.$emit('update', {
        section: 'invoice',
        participant: p,
      })
    },

    photoParticipant(p) {
      this.$emit('update', {
        section: 'photo',
        participant: p,
      })
    },

    printParticipant(p){
      var s = this.selection || [];
      s.push(p)
      this.$emit('update', {
        text: 'Particpant added to print selection',
        selection: s,
      })
    },

    search () {
      this.getAttendees();
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
    this.getAttendees();
  },

  watch: {
    ts: function(){
      this.getAttendees();
    }
  }

}
</script>

<style scoped>

</style>