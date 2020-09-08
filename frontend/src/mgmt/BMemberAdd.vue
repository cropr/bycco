<template>
<v-container grid-list-md class="elevation-1">
  <v-row>
    <v-col cols=9>
      <h1>New member</h1>
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
    <v-col cols=12 sm=6>
      <v-text-field label="First name" v-model="first_name" />
      <v-text-field label="Email" v-model="email" />
      <v-checkbox label="Email publicly visible" v-model="showemail" />
    </v-col>
    <v-col col=12 sm=6>
      <v-text-field label="Last Name" v-model="last_name" />
      <v-text-field label="Mobile" v-model="mobile" />
      <v-checkbox label="Mobile publicly visible" v-model="showmobile" />
    </v-col>
  </v-row>
</v-container>
</template>

<script>

import { mapState } from 'vuex'
import { bearertoken } from "@/util/token"


export default {
  
  name: "BMemberAdd",

  data () {return {
    first_name: '',
    last_name: '',
    email: '',
    mobile: '',
    showemail: true,
    showmobile: true
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
      this.api.create_board_member({}, {
        requestBody: {
          first_name: this.first_name,
          last_name: this.last_name,
          email: this.email,
          mobile: this.mobile,
        },
        securities: bearertoken(this.token),
      }).then(
        function(rc){
          self.$root.$emit('snackbar', {text: 'Boardmember created'})
          self.$router.push('/mgmt/bmember/edit/' + rc.obj)
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

.dropbox {
  width: 100%;
  height: 100px;
}

</style>