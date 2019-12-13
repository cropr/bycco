<template>
<v-container fluid>
  <v-row align="start">
    <v-col cols="12" md=6 offset-md=3 lg=6 offset-lg=3>
      <v-card>
        <v-card-title>
          <v-icon large>perm_identity</v-icon>
          <label class="headline ml-3">Login</label>
          <v-spacer />
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text>
          <v-col cols="12">
            <v-text-field xs="12" lg="4" v-model="login.username" 
              :label="Username">
            </v-text-field>
            <v-text-field xs="12" lg="6" v-model="login.password" 
              :label="Password" type="password">
            </v-text-field>
          </v-col>
          <v-card-actions>
            <v-spacer />
            <v-btn @click="dologin()">Login</v-btn>
            <v-btn text small>Forgot password?</v-btn>
          </v-card-actions>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</v-container>
</template>

<script>
import api from "@/util/api"
// import {mapState} from 'vuex'

export default {
  name: "LoginBoard",

  data(){
    return{
      login: {}
    }
  },
  
  methods: {
    dologin() {
      api('login', {
        "command": "getToken",
        "username": this.login.username,
        "password": this.login.password
      }).then(
        function (data) {
          this.$store.commit('updateToken', data.token);
          if (this.electionEvent && this.electionEvent.id) {
            this.$router.push('/event/' + this.electionEvent.id);
          }
          else {
            this.$router.push('/events');
          }
        }.bind(this),
        function (data) {
          if(data.code == 401) {
            this.$root.$emit('errorDialogOpen', {errortitle: this.$t('Username or password are wrong'),
            errormessage: this.$t('Error in contacting the server, please retry. If the error persists contact the system administrator.')})
          }
        }.bind(this))
    }
  }
}
</script>

<style scoped>

</style>