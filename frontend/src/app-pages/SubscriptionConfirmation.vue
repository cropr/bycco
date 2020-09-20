<template>
<div>
  <h2>{{$t('Confirmation details')}}</h2>
  <v-row>
    <v-col cols=12 sm=6>
      <div class="mt-2">
        <span>{{$t('Full name')}}</span>:
        {{ subscription.first_name }} {{subscription.last_name}}
      </div>
      <div class="mt-2">
          <span>{{$t('Birthdate')}}</span>:
          {{ subscription.birthdate }}
      </div>
      <div class="mt-2">
          <span>{{$t('ID Club')}}</span>:
          {{ subscription.idclub }}
      </div>
      <div class="mt-2">
          <span>{{$t('Nationality')}}</span>:
          {{ subscription.nationality }}
      </div>
      <div class="mt-2">
        <span>{{$t('Can become Belgian champion')}}</span>:
        <span v-if="subscription.natstatus == 'fidebelg'">{{$t('Yes')}}</span>
        <span v-if="subscription.natstatus == 'nobelg'">{{$t('No')}}</span>
        <span v-if="subscription.natstatus == 'maybe'">{{$t('To be confirmed')}}</span>
      </div>
    </v-col>
    <v-col cols=12 sm=6>
      <div class="mt-2">
          <span>{{$t('National rating')}}</span>:
          {{ subscription.ratingbel }}
      </div>
      <div class="mt-2">
          <span>{{$t('FIDE rating')}}</span>:
          {{ subscription.ratingfide }}
      </div>
      <div class="mt-2">
          <span>{{$t('Gender')}}</span>:
          {{ subscription.gender }}
      </div>
      <div class="mt-2">
          <span>{{$t('Category')}}</span>:
          -{{ subscription.category }}
      </div>
    </v-col>
  </v-row>
  <h2>{{$t('Payment')}}</h2>
  <div v-show="!flow.isConfirmed">
    <div>
      {{ $t('The registration fee is 35 Euro.') }}
    </div>
    <div>
      <v-btn @click="confirm" color="primary">
        {{ $t('Confirm') }}
      </v-btn>
    </div>
  </div>
  <div class="mt-2" v-show="flow.isConfirmed">
    <div>
      {{ $t('Your subscription is confirmed') }}
    </div>
    <div>
      {{ $t('Pay the amount to account BE33 0017 5924 5146 before the 25th of October with the structured message:') }}
      {{ subscription.paymessage }}
    </div>
    <div class="mt-2">
      <v-btn @click="restart()">
        {{ $t('New subscription') }}
      </v-btn>
    </div>
  </div>
</div>
</template>

<script>

import { mapState } from 'vuex'

export default {
  name: "SubscriptionConfirmation",

  data () {return {
    errorcode: false,
    paymessage: ''
  }},

  computed: {
    ...mapState(['subscription','api', 'flow']),
  },

  methods: {

    confirm() {
      this.api.anon_confirm_subscription({id: this.subscription.id}).then(
        function(data){
          this.$store.commit('updateSubscription', data.obj);
          this.$store.commit('updateFlow', {isConfirmed: true});
        }.bind(this),
        function(data){
          console.error('Error confirming', data)
        }
      );
    },
    restart () {
      console.log('trying to reinit');
      window.location.reload();
    }

  },
}
</script>
