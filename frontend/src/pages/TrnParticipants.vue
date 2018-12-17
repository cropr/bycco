<template>
  <v-app>
    <sidebar />
    <topbar />
    <v-content><v-container fluid grid-list-lg>
      <h1 class="my-2">{{ $t('Participants') }}</h1>
      <h4>{{ $t('Filter categories')}}</h4>
      <v-layout row wrap>
        <v-flex md1 sm2 xs3 v-for="c in boys" :key="c">
          <v-checkbox v-model="catsSelected[c]" :label="c" hide-details class="check"
                      @change="recalc" />
        </v-flex>
      </v-layout>
      <v-layout row wrap>
        <v-flex md1 sm2 xs3 v-for="c in girls" :key="c">
          <v-checkbox v-model="catsSelected[c]" :label="c" hide-details class="check"
                      @change="recalc" />
        </v-flex>
      </v-layout>
      <v-data-table :items="filteredParticipants" class="elevation-1" :headers="headers"
        :rows-per-page-items="[25,50,100]"
        :rows-per-page-text="$t('Rows per page')"
      >
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
    <bycco-footer />
  </v-app>
</template>

<script>

import api from '../util/api'
import { loadLanguageAsync } from '../util/lang'
import _ from 'lodash'

// import { mapState } from 'vuex'

import Sidebar from '../components/Sidebar'
import Topbar from '../components/Topbar'
import ByccoFooter from '../components/ByccoFooter'
import AdCarousel from '../components/AdCarousel'

export default {

  name: 'TrnParticipants',

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

  created () {
    loadLanguageAsync(window.config.lang);
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
    recalc () {
      let catarray = [];
      _.forEach(this.catsSelected, function(v,k){
        if (v) catarray.push(k)
      });
      this.allcats = !catarray.length;
    }
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

.check {
  margin: 0;
}
</style>