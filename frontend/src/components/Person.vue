<template>
<v-flex xs12 md6 xl4>
  <v-layout row class="ma-3">
    <div class="personleft" >
      <img :src="photourl" class="personphoto">
    </div>
    <v-flex d-flex grow>
      <v-card>
        <v-card-title  class="blue-grey lighten-3">
          {{attendee.first_name}} {{attendee.last_name}}
        </v-card-title>
        <v-card-text>
          <div>tel: {{attendee.mobileplayer}}</div>
          <div>email: {{attendee.emailplayer}}</div>
        </v-card-text>
        <v-card-actions>
          <v-btn flat icon class="blue-grey" :href="'tel:' + attendee.mobileplayer">
            <v-icon color="white">phone</v-icon>
          </v-btn>
          <v-btn flat icon class="blue-grey" :href="'sms:' + attendee.mobileplayer">
            <v-icon  color="white">textsms</v-icon>
          </v-btn>
          <v-btn flat icon  class="blue-grey" :href="'mailto:' + attendee.emailplayer">
            <v-icon color="white">email</v-icon>
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</v-flex>
</template>

<script>

import api from '../util/api';

export default {

  name: 'Person',

  props: ['idsub'],

  computed: {
    photourl () {
      return "/api/subscriptions/" + this.idsub + "/photo"; 
    }, 
  },

  data () {
    return {
      attendee: {}
    }
  },

  mounted () {
    api('getAttendee', {
      id: this.idsub
    }).then(
      function(data){
        this.attendee = data.attendee;
      }.bind(this), 
      function(data){
        console.log('error getting attendee', data)
      }
    )
  },

}
</script>

<style scoped>

.personleft {
  display: flex;
  flex: 0 0 160px;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

@media only screen and (max-width: 599px) {
  .personleft {
    flex-basis: 120px;
  }
}

.person-right {
  flex: 1 1 auto;
}

.personphoto {
  width: 160px;
}

@media only screen and (max-width: 599px) {
  .personphoto {  
    width: 120px;
  }
}

</style>
