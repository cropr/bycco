<template>
<v-container fluid grid-list-md class="elevation-1">
  <v-layout row>
    <v-flex>
      <h1>Presence Checks</h1>
    </v-flex>
    <v-flex>
      <v-tooltip bottom>
        <v-btn outline fab color="blue-grey" @click="back" slot="activator">
          <v-icon>arrow_back</v-icon>
        </v-btn>
        <span>Go Back</span>
      </v-tooltip>
    </v-flex>
  </v-layout>

  <v-layout row wrap>
    <v-flex md1 sm2 xs3 v-for="c in cats" :key="c">
      <v-checkbox :label="c" v-model="selcats[c]" @change="reload" hide-details/>
    </v-flex>
  </v-layout>

  <v-layout row>

    <v-flex md6 s12 xs12>
      <h4>Not presented yet</h4>
      <v-data-table :items="notpresent" class="elevation-1" :headers="headers_np"
                    :rows-per-page-items="[25,50,100]"  :pagination.sync="pag_np">
        <template slot="headers" slot-scope="props" >
          <th v-for="header in props.headers" :key="header.text" @click="changeSortNp(header)">
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
            <v-icon class="mr-1" @click="setPresence(props.item)">check</v-icon>
          </td>
        </template>
      </v-data-table>
    </v-flex>
    <v-flex md6 s12 xs12>
      <h4>presented</h4>
      <v-data-table :items="present" class="elevation-1" :headers="headers_p"
                    :rows-per-page-items="[25,50,100]"  :pagination.sync="pag_p">
        <template slot="headers" slot-scope="props" >
          <th v-for="header in props.headers" :key="header.text" @click="changeSortP(header)">
            {{ header.text }}
            <v-icon small v-show="header.sortable">arrow_upward</v-icon>
          </th>
          <th class="text-xs-left">Actions</th>
        </template>
        <template slot="items" slot-scope="props">
          <td>{{ props.item.id }}</td>
          <td>{{ props.item.first_name }}</td>
          <td>{{ props.item.last_name }}</td>
          <td class="text-xs-center"><date-formatted :date="props.item.present"/></td>
          <td>
            <v-icon class="mr-1" @click="undoPresence(props.item)">undo</v-icon>
          </td>
        </template>
      </v-data-table>
    </v-flex>

  </v-layout> 

</v-container>
</template>

<script>

import api from '../util/api'
import DateFormatted from "./DateFormatted"


export default {
  name: "MgmtPartPresence",

  components: {
    DateFormatted,
  },  

  computed: {
    headers_np () { return [
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
    headers_p () { return [
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
        text: 'Presence',
        align: 'center',
        value: 'present'
      },
    ]},

  },


  data () {return {
    cats: ['B8','G8', 'B10', 'G10', 'B12', 'G12', 'B14', 'G14', 'B16', 'G16',
        'B18', 'G18', 'B20', 'G20', 'IMT', 'ORG', 'ARB', 'EAT'
    ],
    selcats: {},
    notpresent: [],
    pag_np: {
      sortBy: 'last_name',
      descending: false,
    },
    pag_p: {
      sortBy: 'last_name',
      descending: false,
    },    
    present: [],
  }},

  methods: {

    back () {
      this.$emit('update', {section: 'list'})
    },

    changeSortNp (header) {
      if (!header.sortable) return;
      if (this.pag_np.sortBy === header.value) {
        this.pag_np.descending = !this.pag_np.descending
      } else {
        this.pag_np.sortBy = header.value;
        this.pag_np.descending = false
      }
    },    

    changeSortP (header) {
      if (!header.sortable) return;
      if (this.pag_p.sortBy === header.value) {
        this.pag_p.descending = !this.pag_p.descending
      } else {
        this.pag_p.sortBy = header.value;
        this.pag_p.descending = false
      }
    },    

    reload () {
      var sc = [];
      this.cats.forEach(function(c){
        if (this.selcats[c]) {
          sc.push(c)
        }
      }.bind(this))
      this.notpresent = [],
      this.present = [],
      api('getAttendees', {
        cat: sc.join(',')
      }).then(
        function(data){
          data.attendees.forEach(function(p){
            if (p.present) {
              p.present =new Date(p.present)
              this.present.push(p)
            }
            else {
              this.notpresent.push(p)
            }
          }.bind(this));
        }.bind(this), 
        function(data){
          console.error('getAttendees failed ', data)
        })    
    },

    setPresence(p) {
      console.log('set present', p.last_name, p.first_name)
      api('updateAttendee', {
        id: p.id,
        attendee: {
          present: (new Date()).toJSON()
        }
      }).then(
        function(){
          this.reload()
        }.bind(this), 
        function(data){
          console.error('update Presence failed', data);
        } 
      )
    },

    undoPresence(p) {
      console.log('set present', p.last_name, p.first_name)      
      api('updateAttendee', {
        id: p.id,
        attendee: {
          present: null
        },
      }).then(
        function(){
          this.reload()
        }.bind(this), 
        function(data){
          console.error('update Presence failed', data);
        } 
      )    }

  },

  mounted () {
    this.reload();
  },


}
</script>

<style scoped>

</style>