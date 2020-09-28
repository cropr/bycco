<template>
  <v-app>
    <sidebar />
    <topbar />
    <v-content><v-container>
      <h1>{{ $t('Participants')}}</h1>
      <v-data-table :items="filteredParticipants" class="elevation-1" :headers="headers"
      >
        <template v-slot:top>
          <div class="pa-2">
            <h4>{{ $t('Filter categories')}}</h4>
            <v-row>
              <v-col md1 sm2 xs3 v-for="c in boys" :key="c">
                <v-checkbox v-model="catsSelected[c]" :label="c" hide-details class="check"
                            @change="recalc" />
              </v-col>
            </v-row>
            <v-row>
              <v-col md1 sm2 xs3 v-for="c in girls" :key="c">
                <v-checkbox v-model="catsSelected[c]" :label="c" hide-details class="check"
                            @change="recalc" />
              </v-col>
            </v-row>          

          </div>
        </template>      
        <template slot="items" slot-scope="props">
          <td >{{ props.item.last_name }}</td>
          <td >{{ props.item.first_name }}</td>
          <td class="text-xs-center">{{ props.item.gender }}</td>
          <td class="text-xs-center">{{ props.item.category }}</td>
          <td class="text-xs-right">{{ props.item.ratingfide }}</td>
          <td class="text-xs-right">{{ props.item.ratingbel }}</td>
        </template>
      </v-data-table>
    </v-container></v-content>
    <ad-carousel />
    <bycco-footer />
  </v-app>
</template>

<script>

import api from '@/util/api'
import _ from 'lodash'
// import { mapState } from 'vuex'
import Sidebar from '@/components/Sidebar'
import Topbar from '@/components/Topbar'
import ByccoFooter from '@/components/ByccoFooter'
import AdCarousel from '@/components/AdCarousel'

export default {

  name: 'Participants',

  components: {
    Sidebar,
    Topbar,
    ByccoFooter,
    AdCarousel,
  },

  computed: {
    filteredParticipants () {
      if (this.allcats)
        return this.participants;
      return _.filter(this.participants, function(p){
        return this.catsSelected[p.category]
      }.bind(this))
    },
    headers () { return [
      {
        text: this.$t('Last name'),
        sortable: true,
        align: 'left',
        value: 'last_name'
      },
      {
        text: this.$t('First name'),
        sortable: true,
        align: 'left',
        value: 'first_name'
      },
      {
        text: this.$t('Gender'),
        sortable: true,
        align: 'center',
        value: 'gender'
      },
      {
        text: this.$t('Category'),
        sortable: true,
        align: 'center',
        value: 'category'
      },
      {
        text: this.$t('FIDE rating'),
        sortable: true,
        align: 'right',
        value: 'ratingfide'
      },
      {
        text: this.$t('BEL rating'),
        sortable: true,
        align: 'right',
        value: 'ratingbel'
      },
    ]},
  },

  data () {return {
    allcats: true,
    boys: ['B8', 'B10', 'B12', 'B14', 'B16', 'B18', 'B20'],
    catsSelected: {},
    girls:  ['G8', 'G10', 'G12', 'G14', 'G16', 'G18', 'G20'],
    rowsperpage: [25,50,100],
    participants: [],
  }},

  methods: {

    getAttendees () {
      api('getAttendees', {
        confirmed: 1,
      }).then(
        function(data) {
          this.participants = data.attendees;
        }.bind(this)
      );
    },

    recalc () {
      let catarray = [];
      _.forEach(this.catsSelected, function(v,k){
        if (v) catarray.push(k)
      });
      this.allcats = !catarray.length;
    }
  },

  mounted () {
    this.getAttendees()
  },

}
</script>

<style scoped>

.check {
  margin: 0;
}
</style>