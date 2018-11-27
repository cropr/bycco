<template>
  <div>
    <h3>Tekst</h3>
    <p>Lorem Ipsum is slechts een proeftekst uit het drukkerij- en zetterijwezen. Lorem Ipsum is de standaard proeftekst in deze bedrijfstak sinds de 16e eeuw, toen een onbekende drukker een zethaak met letters nam en ze door elkaar husselde om een font-catalogus te maken. Het heeft niet alleen vijf eeuwen overleefd maar is ook, vrijwel onveranderd, overgenomen in elektronische letterzetting. Het is in de jaren '60 populair geworden met de introductie van Letraset vellen met Lorem Ipsum passages en meer recentelijk door desktop publishing software zoals Aldus PageMaker die versies van Lorem Ipsum bevatten.</p>
  </div>
  <!--<v-app>-->
    <!--<sidebar />-->
    <!--<topbar />-->
    <!--<v-content><v-container fluid grid-list-lg>-->
      <!--<h1 class="my-2" v-t="'Subscription'"></h1>-->
      <!--<v-stepper v-model="flow.step" vertical>-->

          <!--<v-stepper-step :complete="flow.step > 1" step="1">-->
            <!--Intro-->
          <!--</v-stepper-step>-->
          <!--<v-stepper-content step="1">-->
            <!--<subscription-intro ></subscription-intro>-->
          <!--</v-stepper-content>-->

          <!--<v-stepper-step :complete="flow.step > 2" step="2">-->
            <!--{{ $t('ID number')}}-->
          <!--</v-stepper-step>-->
          <!--<v-stepper-content step="2">-->
             <!--<subscription-id-number></subscription-id-number>-->
          <!--</v-stepper-content>-->

          <!--<v-stepper-step :complete="flow.step > 3" step="3">-->
            <!--{{ $t('Details')}}-->
          <!--</v-stepper-step>-->
          <!--<v-stepper-content step="3">-->
             <!--<subscription-details></subscription-details>-->
          <!--</v-stepper-content>-->

          <!--<v-stepper-step :complete="flow.step > 4" step="4">-->
            <!--{{ $t('Photo')}}-->
          <!--</v-stepper-step>-->
          <!--<v-stepper-content step="4">-->
             <!--<subscription-photo></subscription-photo>-->
          <!--</v-stepper-content>-->

          <!--<v-stepper-step :complete="flow.step > 5" step="5">-->
            <!--{{ $t('Nationality')}}-->
          <!--</v-stepper-step>-->
          <!--<v-stepper-content step="5">-->
            <!--<subscription-nationality></subscription-nationality>-->
          <!--</v-stepper-content>-->

          <!--<v-stepper-step :complete="flow.confirmed" step="6">-->
            <!--{{ $t('Confirmation')}}-->
          <!--</v-stepper-step>-->
          <!--<v-stepper-content step="6">-->

            <!--<subscription-confirmation></subscription-confirmation>-->
          <!--</v-stepper-content>-->

      <!--</v-stepper>-->
    <!--</v-container></v-content>-->
    <!--<bycco-footer />-->
  <!--</v-app>-->
</template>

<script>

import { loadLanguageAsync } from './util/lang'
import { mapState } from 'vuex'

import Sidebar from './components/Sidebar'
import Topbar from './components/Topbar'
import ByccoFooter from './components/ByccoFooter'
import SubscriptionIntro from './components/SubscriptionIntro'
import SubscriptionIdNumber from './components/SubscriptionIDNumber'
import SubscriptionDetails from './components/SubscriptionDetails'
import SubscriptionPhoto from './components/SubscriptionPhoto'
import SubscriptionNationality from './components/SubscriptionNationality'
import SubscriptionConfirmation from './components/SubscriptionConfirmation'

// import AdCarousel from './components/AdCarousel'

export default {

  name: 'Subscribe',

  computed: {
      ...mapState(['flow'])
  },

  components: {
    Sidebar,
    Topbar,
    ByccoFooter,
    // 'ad-carousel': AdCarousel,
    SubscriptionIntro,
    SubscriptionIdNumber,
    SubscriptionDetails,
    SubscriptionPhoto,
    SubscriptionNationality,
    SubscriptionConfirmation,
  },

  created () {
    loadLanguageAsync(window.config.lang);
  },

}
</script>

<style scoped>

</style>