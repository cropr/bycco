<template>
<div>
  <h2 v-t="'ID number'"></h2>
  <div v-t="'SubId1'"></div>
  <v-text-field :label="$t('ID number')" required v-model="flow.idnumber"></v-text-field>
  <v-btn @click="lookup()" v-t="'Lookup ID number'" color="primary"></v-btn>
  <v-alert type="error" class="mt-2" v-show="errorcode">
    <div v-show="errorcode == 'notfound'">
      <div v-t="'SubId2'"></div>
      <div v-t="'SubId3'"></div>
    </div>
    <div v-show="flow.errorcode == 'playeradult'" v-t="'SubId4'"></div>
    <div v-show="flow.errorcode == 'alreadyregistered'" v-t="'SubId5'"></div>
    <div v-show="flow.errorcode == 'unknown'" v-t="'UnknownError'"></div>
  </v-alert>
  <div class="mt-4">
    <div v-show="flow.isPlayerFound">{{$t('Player found:')}} {{subscription.first_name}} {{subscription.last_name}}</div>
    <div class="mt-2">
      <v-btn v-show="flow.isPlayerFound" v-t="'Continue'" @click="next" color="primary"></v-btn>
      <v-btn v-show="flow.isPlayerFound" v-t="'Other player'" @click="restart"></v-btn>
      <v-btn v-t="'Back'" @click="prev"></v-btn>
    </div>
  </div>
</div>
</template>

<script>
import api from '../util/api'
import { mapState } from 'vuex'

export default {

  name: "SubscriptionIDNumber",

  data () {return{
    errorcode: false,
    found: false
  }},

  computed: {
    ...mapState(['subscription', 'flow'])
  },

  methods: {
    restart () {
      this.$store.commit('delSubscription');
      this.$store.commit('updateFlow', {
        isPlayerFound: false,
        idnumber: '',
      });
      this.errorcode = false;
    },

    lookup() {
      this.errorcode = false;
      api('searchIdNational', {idbel: this.flow.idnumber}).then(
        function(player) {
          if (player.alreadysubscribed) {
            this.errorcode = 'alreadyregistered';
            return;
          }
          let db = new Date(player.birthdate);
          if (db.getFullYear() < 1998) {
            this.errorcode = 'playeradult';
            return;
          }
          this.$store.commit('updateFlow', {isPlayerFound: true})
          this.$store.commit('setSubscription', {
            last_name: player.last_name,
            first_name: player.first_name,
            gender: player.gender,
            ratingsbel: player.ratingsbel,
            currentratingbel: player.currentrating,
            nationalitybel: player.nationalitybel,
            birthdate: new Date(player.birthdate),
            idbel: player._id,
            idfide: player.idfide,
            idclub: player.idclub,
            natstatus: 'maybe',
          });
          if (player.idfide && player.idfide.length) {
            api('searchIdFide', {idfide:player.idfide}).then(
              function(player){
                this.$store.commit('updateSubscription',  {
                  ratingsfide: player.ratingsfide,
                  nationalityfide: player.nationalityfide,
                  chesstitle: player.chesstitle,
                  currentratingfide: player.currentrating,
                  natstatus:  (player.nationalityfide == 'BEL') ? 'fidebelg': 'nobelg'
                });
              }.bind(this),
              null
            )
          }
        }.bind(this),
        function(err) {
          this.errorcode = (err.status == 404) ? 'notfound': 'unknown';
        }.bind(this)
      );
    },

    next () {
      this.$store.commit('updateFlow', {step: this.flow.step+1})
    },

    prev () {
      this.$store.commit('updateFlow', {step: this.flow.step-1})
    },

  }
}
</script>

<style scoped>

</style>