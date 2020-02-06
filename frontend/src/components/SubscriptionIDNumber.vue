<template>
<div>
  <h2>{{$t('ID number')}}</h2>
  <div>{{$t('SubId1')}}</div>
  <v-text-field :label="$t('ID number')" required v-model="flow.idnumber"></v-text-field>
  <v-btn @click="lookup()" color="primary">{{$t('Lookup ID number')}}</v-btn>
  <v-alert type="error" class="mt-2" v-show="errorcode">
    <div v-show="errorcode == 'notfound'">
      <div>{{$t('SubId2')}}</div>
      <div>{{$t('SubId3')}}</div>
    </div>
    <div v-show="errorcode == 'playeradult'">{{$t('SubId4')}}</div>
    <div v-show="errorcode == 'alreadyregistered'">{{$t('SubId5')}}</div>
    <div v-show="errorcode == 'unknown'">{{$t('UnknownError')}}</div>
  </v-alert>
  <div class="mt-4">
    <div v-show="flow.isPlayerFound">{{$t('Player found:')}} {{subscription.first_name}} {{subscription.last_name}}</div>
    <div class="mt-2">
      <v-btn v-show="flow.isPlayerFound" @click="next" color="primary">{{$t('Continue')}}</v-btn>
      <v-btn class="ml-2" v-show="flow.isPlayerFound" @click="restart">{{$t('Other player')}}</v-btn>
      <v-btn class="ml-2" @click="prev">{{$t('Back')}}</v-btn>
    </div>
  </div>
</div>
</template>

<script>
import api from '@/util/api'
import {categories} from '@/util/const'
import { mapState } from 'vuex'

export default {

  name: "SubscriptionIDNumber",

  data () {return{
    errorcode: false,
    found: false,
    maxyear: categories[0].year
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
      api('getSubscription', {
        id: this.flow.idnumber,
        idtype: 'bel',
      }).then(
        function(data){
          if (data.subscription.confirmed) {
            this.errorcode = 'alreadyregistered';
          }
          else  {
            this.$store.commit('updateFlow', {isPlayerFound: true})
            this.$store.commit('setSubscription', data.subscription)
          }
        }.bind(this),
        function(data){
          if (data.status == 404) {
            this.fetchPlayer();
          }
          else {
            this.errorcode = 'unknown';
          }
        }.bind(this)
      );
    },
    
    fetchPlayer(){
      api('searchIdNational', {idbel: this.flow.idnumber}).then(
        function(data) {
          let player = data.belplayer;
          let db = new Date(player.birthdate);
          if (db.getFullYear() < this.maxyear) {
            this.errorcode = 'playeradult';
            return;
          }
          this.$store.commit('updateFlow', {isPlayerFound: true})
          this.$store.commit('setSubscription', {
            birthdate: new Date(player.birthdate),
            last_name: player.last_name,
            first_name: player.first_name,
            gender: player.gender,
            ratingsbel: player.ratingsbel,
            currentratingbel: player.currentratingbel,
            nationalitybel: player.nationalitybel,
            idbel: player._id,
            idfide: player.idfide,
            idclub: player.idclub,
            natstatus: 'maybe',            
          });
          if (player.idfide && player.idfide.length) {
            api('searchIdFide', {idfide:player.idfide}).then(
              function(data){
                let player = data.fideplayer;
                this.$store.commit('updateSubscription',  {
                  ratingsfide: player.ratingsfide,
                  nationalityfide: player.nationalityfide,
                  chesstitle: player.chesstitle,
                  currentratingfide: player.currentratingfide,
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