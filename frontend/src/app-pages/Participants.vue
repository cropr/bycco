<template>
  <v-container fluid grid-list-lg>

    <h1>{{ $t('Participants')}}</h1>
    <v-data-table :items="participants" class="elevation-1" :headers="headers"
        dense  :footer-props="footerprops">
      <template v-slot:top>
        <div class="pa-2">
          <h4>{{ $t('Filter categories')}}</h4>
          <v-row>
            <v-col md1 sm2 xs3 v-for="c in boys" :key="c">
              <v-checkbox v-model="catsSelected[c]" :label="c" 
                hide-details class="check" @change="getParticipants" />
            </v-col>
          </v-row>
          <v-row>
            <v-col md1 sm2 xs3 v-for="c in girls" :key="c">
              <v-checkbox v-model="catsSelected[c]" :label="c" hide-details 
                class="check" @change="getParticipants" />
            </v-col>
          </v-row>          

        </div>
      </template>
      <template #item.index="{ item }">
        {{ participants.indexOf(item) + 1}}
      </template>            
    </v-data-table>
  </v-container>
</template>

<script>

import { mapState } from 'vuex'

export default {

  name: 'Participants',

  computed: {
    ...mapState(['locale', 'api']),
    headers () { return [
      {
        text: 'N',
        sortable: true,
        align: 'left',
        value: 'index'
      },
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
    boys: ['B8', 'B10', 'B12', 'B14', 'B16', 'B18', 'B20'],
    catsSelected: {},
    girls:  ['G8', 'G10', 'G12', 'G14', 'G16', 'G18', 'G20'],
    footerprops: {
      "items-per-page-options": [20, 50, -1],
    },
    participants: [],
  }},

  methods: {

    getParticipants () {
      let self=this, cs=[], cat;
      this.boys.forEach(c => {if (this.catsSelected[c]) cs.push(c)} );
      this.girls.forEach(c => {if (this.catsSelected[c]) cs.push(c)} );
      console.log('cs', cs)
      cat = cs.length ? cs.join(',') : 'all';
      this.api.anon_get_participants({
        cat: cat
      }).then(
        function(data) {
          self.participants = data.obj.subscriptions;
        }
      );
    },

  },

  mounted () {
    this.getParticipants()
  },

}
</script>

<style scoped>

.check {
  margin: 0;
}
</style>