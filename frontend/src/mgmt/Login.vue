<template>
<v-container fluid>
  <v-row align="start">
    <v-col cols="12" md=6 offset-md=3 lg=6 offset-lg=3>
      <v-card>
        <v-card-title>
          <v-icon large>mdi-account</v-icon>
          <label class="headline ml-3">Login</label>
          <v-spacer />
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text>
          <v-col cols="12">
              <g-signin-button :params="googleSignInParams" @success="onSignInSuccess" @error="onSignInError">
              </g-signin-button>
          </v-col>
          <!-- <v-col cols="12">
            <v-text-field xs="12" lg="4" v-model="login.username" 
              label="Username">
            </v-text-field>
            <v-text-field xs="12" lg="6" v-model="login.password" 
              label="Password" type="password">
            </v-text-field>
          </v-col>-->
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</v-container>
</template>

<script>
import Vue from 'vue'
import GSignInButton from 'vue-google-signin-button'
import { mapState } from 'vuex'

Vue.use(GSignInButton)

export default {
  name: "Login",

  data(){
    return{
      login: {},
      googleSignInParams: {
        client_id: "767432590119-itkr36suu2qn41irsf5ie3mekfqdgt1q.apps.googleusercontent.com"
      }      
    }
  },
  
  computed: {
    ...mapState(['token', 'api'])
  },

  methods: {

    onSignInSuccess (googleUser) {
      let self = this;
      let id_token = googleUser.getAuthResponse().id_token;
      this.api.login({}, {
        requestBody: {
          logintype: 'google',
          token: id_token
        }
      }).then(
        function(data){
          self.$store.commit('updateToken', data.obj)
          self.$router.push('/mgmt/page/list')
        },
        function(data){
          console.log('failed login', data)
        },
      )
    },

    onSignInError (error) {
      console.log('Google login failed', error)
    },

    dologin() {

    }
  }
}
</script>

<style scoped>

.g-signin-button {
   height: 46px;
   width: 191px;
   background-image: url('~@/assets/img/btn_google_signin_light_normal_web.png');
} 

.g-signin-button:hover {
   background-image: url('~@/assets/img/btn_google_signin_light_focus_web.png');
} 


</style>