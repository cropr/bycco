<template>

    <v-container fluid grid-list-lg>

      <h1 class="my-2">{{$t('Subscription')}}</h1>
    
      <v-stepper v-model="flow.step" vertical >

        <v-stepper-step :complete="flow.step > 1" step="1">
          Intro
        </v-stepper-step>
        <v-stepper-content step="1">
          <subscription-intro />
        </v-stepper-content>

        <v-stepper-step :complete="flow.step > 2" step="2">
          {{ $t('ID number')}}
        </v-stepper-step>
        <v-stepper-content step="2">
            <subscription-id-number />
        </v-stepper-content>

        <v-stepper-step :complete="flow.step > 3" step="3">
          {{ $t('Details')}}
        </v-stepper-step>
        <v-stepper-content step="3">
            <subscription-details :subcat="subcat" />
        </v-stepper-content>

        <v-stepper-step :complete="flow.step > 4" step="4">
          {{ $t('Nationality')}}
        </v-stepper-step>
        <v-stepper-content step="4">
          <subscription-nationality />
        </v-stepper-content>

        <v-stepper-step :complete="flow.confirmed" step="5">
          {{ $t('Confirmation')}}
        </v-stepper-step>
        <v-stepper-content step="5">
          <subscription-confirmation />
        </v-stepper-content>

      </v-stepper>
    
    </v-container> 

</template>

<script>

import { mapState } from "vuex"

import SubscriptionIntro from './SubscriptionIntro'
import SubscriptionIdNumber from './SubscriptionIDNumber'
import SubscriptionDetails from './SubscriptionDetails'
import SubscriptionNationality from './SubscriptionNationality'
import SubscriptionConfirmation from './SubscriptionConfirmation'

export default {

  name: 'Subscription',

  components: {
    SubscriptionIntro,
    SubscriptionIdNumber,
    SubscriptionDetails,
    SubscriptionNationality,
    SubscriptionConfirmation,    
  },

  data () {return {
     subcat: ''
  }},

  computed: {
    ...mapState(['locale', 'api', 'flow', 'subscription']),
  },

}
</script>


<style scoped>

</style>
