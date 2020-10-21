<template>
<v-container>
  <h1>Edit Swar Tournament </h1>
  <v-card>
    <v-card-title color="grey lighten-4">
      {{ t.name }}
      <v-spacer />
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" outlined fab color="deep-purple" @click="back()" 
              slot="activator">
            <v-icon>mdi-arrow-left</v-icon>
          </v-btn>
        </template>
        <span>Go Back</span>
      </v-tooltip>
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" outlined fab color="deep-purple" @click="save()" 
              slot="activator">
            <v-icon>mdi-content-save</v-icon>
          </v-btn>
        </template>
        <span>Save Torunament</span>
      </v-tooltip>
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" outlined fab color="deep-purple" @click="remove()" 
              slot="activator">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </template>
        <span>Delete Tournament</span>
      </v-tooltip>
    </v-card-title>
    <v-card-text>
      <v-text-field label="Name" v-model="t.name" />
    </v-card-text>
  </v-card>
</v-container>
</template>

<script>

import { mapState } from 'vuex'
import { bearertoken } from "@/util/token"

export default {

  name: "SwarTrnEdit",


  computed: {
    ...mapState(['token', 'api']),
  },

  data () {return {
    dialogDelete : false,
    idtrn: this.$route.params.id,
    t: {},
  }},

  methods: {

    back () {
      this.$router.push('/mgmt/swartrn/list');
    },

    getSwarTrn() {
      let self=this;
      console.log('getting swartrn')
      this.api.getSwarTrn(
        {id: this.$route.params.id},
        {securities: bearertoken(this.token)},
      ).then(
        function(data) {
          console.log('got trn', data.obj)
          self.t = data.obj;
        },
        function(data){
          console.error('failed get swartrn', data)
          self.$root.$emit('snackbar', {text: 'Getting swartrn failed', reason: data})          
        }
      );
    },



    remove() {
      let self=this;
      if (window.confirm('Are you sure to delete tournamant "' + this.name + '"?')) {
        this.api.deleteSwarTrn(
          {id: this.$route.params.id },        
          {securities: bearertoken(this.token)}, 
        ).then(
          function(){
            self.$root.$emit('snackbar', {text: 'Page deleted'})
            self.back();
          }, 
          function(data){
            // TODO show error message
            console.error('failed to delete', data);
            self.$root.$emit('snackbar', {text: 'Delete swar trn failed', reason: data})
          }
        );
      }
    },

    save () {
      this.api.update_page({id: this.idpage}, {
        requestBody: {
          name: this.t.name,
          shortname: this.t.shortname,
          swarname: this.t.swarname,
          rounds: this.t.rounds
        },
        securities: bearertoken(this.token),
      }).then(
        function () {
          self.$root.$emit('snackbar', {text: 'Swar trn saved'})
          self.back();
        },
        function (data) {
          console.error('failed to delete', data);
          self.$root.$emit('snackbar', {text: 'Update swar trn failed', reason: data})
        }
      )      
    },

  },

  mounted () {
    this.getSwarTrn();
  }

}
</script>

<style scoped>
.bordermd {
  border: 1px solid grey;
}
</style>