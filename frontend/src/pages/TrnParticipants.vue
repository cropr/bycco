<template>
  <v-app>
    <sidebar />
    <topbar />
    <v-content><v-container fluid grid-list-lg>
      <h1 class="my-2">{{ $t('Participants') }}</h1>
      <v-data-table :items="filteredParticipants" class="elevation-1" :headers="headers"
        :rows-per-page-items="[10,25,50,100]"
        :rows-per-page-text="$t('Rows per page')"
      >
        <template slot="items" slot-scope="props">
          <td >{{ props.item.last_name }}</td>
          <td >{{ props.item.first_name }}</td>
          <td class="text-xs-center">{{ props.item.gender }}</td>
          <td class="text-xs-center">{{ props.item.category }}</td>
          <td class="text-xs-right">{{ props.item.ratingbel }}</td>
          <td class="text-xs-right">{{ props.item.ratingfide }}</td>
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
      return _.filter(this.participants, {category: 'B10'})
    }
  },

  created () {
    loadLanguageAsync(window.config.lang);
  },

  data () {return{
    headers: [
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
        text: this.$t('FIDE Rating'),
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
    ],
    rowsperpage: [25,50,100],
    participants: [],
  }},

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