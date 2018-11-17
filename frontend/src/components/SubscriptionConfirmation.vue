<template>
<div>
  <h2 v-t="'Confirmation details'"></h2>
  <v-layout row>
    <v-flex xs12 sm6 lg4 class="confirmationphoto">
      <img :src="photo">
    </v-flex>
    <v-flex xs12 sm6 lg4>
      <div class="mt-2">
        <span v-t="'Full name'"></span>:
        {{ subscription.first_name }} {{subscription.last_name}}
      </div>
      <div class="mt-2">
          <span v-t="'Birthdate'"></span>:
          {{ birthdate }}
      </div>
      <div class="mt-2">
          <span v-t="'ID Club'"></span>:
          {{ subscription.id_club }}
      </div>
      <div class="mt-2">
          <span v-t="'Nationality'"></span>:
          {{ subscription.nationalitybel }}
      </div>
      <div class="mt-2">
          <span v-t="'FIDE Nationality'"></span>:
          {{ subscription.nationalityfide }}
      </div>
      <div class="mt-2">
        <span v-t="'Can become Belgian champion'"></span>:
        <span v-if="subscription.natstatus == 'fidebelg'" v-t="'Yes'"></span>
        <span v-if="subscription.natstatus == 'nobelg'" v-t="'No'"></span>
        <span v-if="subscription.natstatus == 'maybe'" v-t="'To be confirmed'"></span>
      </div>
    </v-flex>
    <v-flex xs12 sm6 lg4>
      <div class="mt-2">
          <span v-t="'National rating'"></span>:
          {{ subscription.currentratingbel }}
      </div>
      <div class="mt-2">
          <span v-t="'FIDE rating'"></span>:
          {{ subscription.currentratingfide }}
      </div>
      <div class="mt-2">
          <span v-t="'Gender'"></span>:
          {{ subscription.gender }}
      </div>
      <div class="mt-2">
          <span v-t="'Category'"></span>:
          -{{ subscription.category }}
      </div>
    </v-flex>
  </v-layout>
  <h3 v-t="'Payment'"></h3>
  <div v-t="'SubConf1'"></div>
  <div><span v-t="'SubConf2'"></span> {{ subscription.paymessage }}</div>
  <div>
    <v-btn v-t="'Confirm'" @click="confirm" color="primary"></v-btn>
  </div>
  <div v-show="flow.isConfirmed">
    <div v-t="'Your subscription is confirmed'"></div>
    <v-btn v-t="'New subscription'" @click="restart"></v-btn>
  </div>
</div>
</template>

<script>

import api from '../util/api'
import { mapState } from 'vuex'
import { formatDate } from "../util/utils";

export default {
  name: "SubscriptionConfirmation",

  data () {return {
    errorcode: false
  }},

  computed: {
    birthdate () {
      return formatDate(this.subscription.birthdate);
    },
    ...mapState(['subscription','photo', 'flow']),
  },

  methods: {
    confirm() {
      api('confirmSubscription',{
        idsub: this.subscription.idsub
      }).then(
        function(){
          this.$store.commit('updateFlow', {isConfirmed: true});
        }.bind(this),
        function(data){
          console.error('Error confirming', data)
        }
      );
    },
    restart () {
      this.$store.commit('init')
    }
  },
}
</script>

<style scoped>

</style>