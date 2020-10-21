<template>
<v-container>
  <h1>New Swar Tournament</h1>
  <v-card>
    <v-card-title color="grey lighten-4">
      &nbsp;
      <v-spacer />
      <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn v-on="on" @click="back()" fab outlined 
                  color="deep-purple">
              <v-icon>mdi-arrow-left</v-icon>
            </v-btn>
          </template>
          <span>Go Back</span>
      </v-tooltip>
      <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn v-on="on" @click="save()" fab outlined 
                  color="deep-purple">
              <v-icon>mdi-content-save</v-icon>
            </v-btn>
          </template>
          <span>Save changes</span>
      </v-tooltip>
    </v-card-title>
    <v-card-text>
      <v-text-field label="Name" v-model="name" />
      <v-text-field label="Cat" v-model="shortname" />
      <v-text-field label="Rounds" v-model="rounds" type="number" />
    </v-card-text>
  </v-card>
</v-container>
</template>

<script>

import { mapState } from 'vuex'
import { bearertoken } from "@/util/token"

export default {
  
  name: "SwarTrnAdd",

  data () {return {
    name: '',
    rounds: 9,
    shortname: ''
  }},

  computed: {
    ...mapState(['token', 'api'])
  },

  methods: {

    back () {
      this.$router.back();
    },

    save () {
      let self=this;
      this.api.addSwarTrn({}, {
        requestBody: {
          'name': this.name,
          'shortname': this.shortname,
          'rounds': this.rounds
        },
        securities: bearertoken(this.token),
      }).then(
        function(data){
          self.$root.$emit('snackbar', {text: 'Swar Trn created'})
          self.$router.push('/mgmt/swar/edit/'  + data.body)
        },
        function(data){
          console.error('failed to save', data);
        }
      );
    },
  },


}
</script>

<style scoped>

.dropbox {
  width: 100%;
  height: 100px;
}

</style>