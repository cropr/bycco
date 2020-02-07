<template>
<v-container>
  <h1>Management Participants</h1>
  <v-data-table :items="filteredParticipants" class="elevation-1" 
      :headers="headers" >
    <template v-slot:top>
      <v-toolbar flat color="white">
        <v-toolbar-title>
          Particpiants
        </v-toolbar-title>
        <v-spacer></v-spacer>
        <v-tooltip bottom >
          <template v-slot:activator="{ on }">
            <v-btn v-on="on" @click="addParticipant()" fab outlined 
                  color="deep-purple">
              <v-icon>add</v-icon>
            </v-btn>
          </template>
          <span>Add Participant</span>
         </v-tooltip>
        <v-tooltip bottom >
          <template v-slot:activator="{ on }">
            <v-btn v-on="on" @click="csvAttendees()" fab outlined 
                  color="deep-purple">
              <v-icon>cloud_download</v-icon>
            </v-btn>
          </template>
          <span>CSV Download</span>
         </v-tooltip>
        <v-tooltip bottom >
          <template v-slot:activator="{ on }">
            <v-btn v-on="on" @click="gotoBadge()" fab outlined 
                  color="deep-purple">
              <v-icon>assignment_ind</v-icon>
            </v-btn>
          </template>
          <span>CSV Download</span>
         </v-tooltip>
      </v-toolbar>
      <v-row row wrap>
        <v-col>
          <v-text-field append-icon="search" @click:append="search" v-model="ss" />
        </v-col>
        <v-col>
          <v-select :items="catitems" v-model="catselected" @change="changeCat()" />
        </v-col>
        <v-col>
          <v-checkbox label="Not confirmed" v-model="isNotConfirmed" />
        </v-col>
      </v-row>
    </template>
    <template v-slot:item.action="{ item }">
      <v-icon small class="mr-2"  @click="editParticipant(item)" >
        edit
      </v-icon>
      <v-icon small class="mr-2"  @click="printParticipant(item)" >
        print
      </v-icon>
    </template>          
  </v-data-table>

</v-container>
</template>

<script>

import api from '@/util/api'
import { mapState } from 'vuex'

import _ from 'lodash'


export default {

  name: "ParticipantList",

  computed: {
    ...mapState(['token', 'participant', 'printselection']),
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
        value: 'subscriptionnumber'
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
      {
        text: 'Actions', value: 'action', sortable: false
      }      
    ]},
    catsearch () {
      if (['All', 'Players'].indexOf(this.catselected) >= 0 ) return null;
      return this.catselected;
    },

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
    isNotConfirmed: false,
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
      this.$router.push('/mgmt/participant/edit/' + p.id)
    },

    csvAttendees () {
      api('getAttendees', {
        cat: this.catsearch,
        ss: this.ss.length ? this.ss : null,
        format: 'csv'
      }).then(
        function(data) {
          console.log('csv attendees', data);
          let link = document.createElement("a");
          link.download = 'subscription.csv';
          link.href = 'data:text/csv;base64,' + btoa(data.attendees);
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
        }.bind(this)
      );
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
      this.$router.push('/mgmt/participant/add')
    },

    gotoBadge () {
      this.$router.push('/mgmt/participant/badge')
    },

    gotoNamecard () {
      this.$router.push('/mgmt/participant/namecard')
    },

    gotoPresence () {
      this.$router.push('/mgmt/participant/presence')
    },

    photoParticipant(p) {
      this.$router.push('/mgmt/participant/photo/' + p.id)
    },

    printParticipant(p){
      this.$emit('addPrintSelection', p);
      this.$emit('showSnackbar', 'Particpant added to print selection');
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