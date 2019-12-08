<template>
<div>
  <h2>{{$t('Confirmation details')}}</h2>
  <v-layout row>
    <v-flex xs12 sm6 lg4 class="confirmationphoto">
      <img :src="photo">
    </v-flex>
    <v-flex xs12 sm6 lg4>
      <div class="mt-2">
        <span>{{$t('Full name')}}</span>:
        {{ subscription.first_name }} {{subscription.last_name}}
      </div>
      <div class="mt-2">
          <span>{{$t('Birthdate')}}</span>:
          {{ birthdate }}
      </div>
      <div class="mt-2">
          <span>{{$t('ID Club')}}</span>:
          {{ subscription.id_club }}
      </div>
      <div class="mt-2">
          <span>{{$t('Nationality')}}</span>:
          {{ subscription.nationalitybel }}
      </div>
      <div class="mt-2">
          <span>{{$t('FIDE Nationality')}}</span>:
          {{ subscription.nationalityfide }}
      </div>
      <div class="mt-2">
        <span>{{$t('Can become Belgian champion')}}</span>:
        <span v-if="subscription.natstatus == 'fidebelg'">{{$t('Yes')}}</span>
        <span v-if="subscription.natstatus == 'nobelg'">{{$t('No')}}</span>
        <span v-if="subscription.natstatus == 'maybe'">{{$t('To be confirmed')}}</span>
      </div>
    </v-flex>
    <v-flex xs12 sm6 lg4>
      <div class="mt-2">
          <span>{{$t('National rating')}}</span>:
          {{ subscription.currentratingbel }}
      </div>
      <div class="mt-2">
          <span>{{$t('FIDE rating')}}</span>:
          {{ subscription.currentratingfide }}
      </div>
      <div class="mt-2">
          <span>{{$t('Gender')}}</span>:
          {{ subscription.gender }}
      </div>
      <div class="mt-2">
          <span>{{$t('Category')}}</span>:
          -{{ subscription.category }}
      </div>
    </v-flex>
  </v-layout>
  <h3>{{$t('Payment')}}</h3>
  <div>{{$t('SubConf1')}}</div>
  <div>
    <v-btn @click="confirm" color="primary">{{$t('Confirm')}}</v-btn>
  </div>
  <div class="mt-2" v-show="flow.isConfirmed">
    <div>{{$t('Your subscription is confirmed')}}</div>
    <div><span>{{$t('SubConf2')}}</span> {{ paymessage }}</div>
    <v-btn @click="restart">{{$t('New subscription')}}</v-btn>
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
    errorcode: false,
    paymessage: ''
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
        function(data){
          this.paymessage = data.paymessage
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