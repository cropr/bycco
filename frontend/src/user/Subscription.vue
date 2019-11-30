<template>

<v-app>

  <sidebar />
  <topbar />
  <v-content>
    <v-container fluid grid-list-lg>
      <h1 class="my-2">{{$t('Subscription')}}</h1>
      <v-stepper v-model="flow.step" vertical>

        <v-stepper-step :complete="flow.step > 1" step="1">
          Intro
        </v-stepper-step>
        <v-stepper-content step="1">
          <subscription-intro ></subscription-intro>
        </v-stepper-content>

        <v-stepper-step :complete="flow.step > 2" step="2">
          {{ $t('ID number')}}
        </v-stepper-step>
        <v-stepper-content step="2">
            <subscription-id-number></subscription-id-number>
        </v-stepper-content>

        <v-stepper-step :complete="flow.step > 3" step="3">
          {{ $t('Details')}}
        </v-stepper-step>
        <v-stepper-content step="3">
            <subscription-details></subscription-details>
        </v-stepper-content>

        <v-stepper-step :complete="flow.step > 4" step="4">
          {{ $t('Photo')}}
        </v-stepper-step>
        <v-stepper-content step="4">
            <subscription-photo></subscription-photo>
        </v-stepper-content>

        <v-stepper-step :complete="flow.step > 5" step="5">
          {{ $t('Nationality')}}
        </v-stepper-step>
        <v-stepper-content step="5">
          <subscription-nationality></subscription-nationality>
        </v-stepper-content>

        <v-stepper-step :complete="flow.confirmed" step="6">
          {{ $t('Confirmation')}}
        </v-stepper-step>
        <v-stepper-content step="6">
          <subscription-confirmation></subscription-confirmation>
        </v-stepper-content>

      </v-stepper>
    </v-container>      

    <ad-carousel/>
    <bycco-footer />
  </v-content>

</v-app>

</template>

<script>

import {mapState} from "vuex"

import Sidebar from '@/components/Sidebar.vue'
import Topbar from '@/components/Topbar.vue'
import ByccoFooter from '@/components/ByccoFooter.vue'
import AdCarousel from '@/components/AdCarousel.vue'
import SubscriptionIntro from '@/components/SubscriptionIntro'
import SubscriptionIdNumber from '@/components/SubscriptionIDNumber'
import SubscriptionDetails from '@/components/SubscriptionDetails'
import SubscriptionPhoto from '@/components/SubscriptionPhoto'
import SubscriptionNationality from '@/components/SubscriptionNationality'
import SubscriptionConfirmation from '@/components/SubscriptionConfirmation'

export default {

  name: 'Subscription',

  components: {
    Sidebar,
    Topbar,
    ByccoFooter,
    AdCarousel,
    SubscriptionIntro,
    SubscriptionIdNumber,
    SubscriptionDetails,
    SubscriptionPhoto,
    SubscriptionNationality,
    SubscriptionConfirmation,    
  },

  computed: {
    ...mapState(['flow'])
  },

}
</script>


<style scoped>

</style>
