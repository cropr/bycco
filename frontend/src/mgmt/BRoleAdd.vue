<template>
<v-container class="elevation-2">
  <v-row>
    <v-col cols=9>
      <h1>New boardrole</h1>
    </v-col>
    <v-col cols=3>
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
    </v-col>
  </v-row>
  <v-row>
    <v-col col=12 sm=6>
      <v-text-field label="Name role" v-model="name" />
    </v-col>
  </v-row>
</v-container>
</template>

<script>

import { mapState } from 'vuex'
import { bearertoken } from "@/util/token"


export default {
  
  name: "BRoleAdd",

  data () {return {
    name: '',
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
      this.api.create_board_role({}, {
        requestBody: {
          name: this.name
        },
        securities: bearertoken(this.token),
      }).then(
        function(rc){
          self.$root.$emit('snackbar', {text: 'Boardrole created'})
          self.$router.push('/mgmt/brole/edit/' + rc.obj)
        },
        function(rc){
          console.error('failed to save', rc);
          // TODO snackbar added
        });
    },
  },

}
</script>

<style scoped>

</style>