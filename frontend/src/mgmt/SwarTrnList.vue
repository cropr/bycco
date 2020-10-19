<template>

<v-container>
  <h1>Management Swar tournaments</h1>
  <v-data-table :headers="headers" :items="filteredpages" :footer-props="footerProps"
      class="elevation-1" :sort-by="['name','modified']">
    <template v-slot:top>
      <v-card color="grey lighten-4">
        <v-card-title>
          <v-spacer />
          <v-tooltip bottom >
            <template v-slot:activator="{ on }">
              <v-btn v-on="on" @click="addPage()" fab outlined 
                    color="deep-purple">
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </template>
            Add Tournament
          </v-tooltip>
        </v-card-title>
      </v-card>
    </template>
    <template v-slot:item.action="{ item }">
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-icon v-on="on" small class="mr-2"  @click="editTrn(item)" >
            mdi-pencil
          </v-icon>
        </template>
        Edit Tournament
      </v-tooltip>
    </template>
    <template v-slot:no-data>
      No tournaments found.
    </template>            
  </v-data-table>
</v-container>

</template>

<script>

import { mapState } from 'vuex'
import { bearertoken } from "@/util/token"

export default {

  name: 'SwarTrnList',

  data () {return {
    filter: {},
    headers: [
      {
        text: "Name", value: 'name'
      },
      {
        text: "Cat", value: 'shortname'
      },
      {
        text: "Rounds", value: 'rounds'
      },
      {
        text: "Swar name", value: 'swarname'
      },
      {
        text: 'Actions', value: 'action', sortable: false
      }
    ],    
    trns: [],
  }},

  computed: {
    ...mapState(['token', 'api']),
  },

  methods: {

    addTrn () {
      this.$router.push('/mgmt/swartrn/add')
    },

    editTrn (item) {
      this.$router.push('/mgmt/swartrn/edit/'  + item.id)
    },
    
    getSwarTrns() {
      let self=this;
      this.api.getSwarTrns(
        {},
        {securities: bearertoken(this.token)},
      ).then(
        function(data) {
          self.trns = data.obj.trns;
        },
        function(data){
          if (data.status == 401) {
            self.$router.push('/mgmt/login')
          }
          else {
            console.error('getting getSwarTrns', data);
            self.$root.$emit('snackbar', {text: 'Getting SwarTrns failed', reason: data})            
          }
        }
      );
    }
    
  },

  mounted () {
    this.getSwarTrns();
  },  

}
</script>
