<template>
<div>
  
  <h2>{{$t('Nationality')}}</h2>
  <div v-show="natstatus == 'fidebelg'">
    {{ $t('For the FIDE you are a Belgian. This means you can win the Belgian title and you can participate at the European and World Championships as part of the Belgian team.') }}
  </div>
  <div v-show="natstatus == 'nobelg'">
    {{ $t('For the FIDE you are not a Belgian. This means you cannot win the Belgian title and you cannot participate to the European and World Championships as part of the Belgian team.') }}
  </div>  
  <div v-show="natstatus == 'maybe'">
    {{ $t('You are not affiliated to the FIDE. Unless you <a href=mailto:info@bycco.be>contact us</a> before the 15th of March and instruct us to explicitely do otherwise, we will affiliate you as a Belgian to the FIDE, so you can win the Belgian title and you can participate to the European and World Championships as part of the Belgian team.') }}
  </div>
  <v-checkbox :label="$t('I agree')" v-model="hasAgreedNat" />

  <h2>{{$t('Privacy rules')}}</h2>
  <div>
    {{$t('You give Bycco the right to use the personal data collected in this subscription form.')}}
  </div>
  <div>
    {{$t('Bycco will only use this data in order to organize these championships.')}}
  </div>
  <ul>
    <li>
      {{$t('Bycco will use all personal data like mobile numbers and email addresses for internal purposes only.')}}
    </li>
    <li>
      {{$t('Bycco is taking overview photos/videos of the championships and can publish these photos/videos on its website and on social media')}}
    </li>
    <li>
      {{$t('If Bycco is taking a close-up photos/video of a player, Bycco will explicitly ask permission to publish.')}}
    </li>
  </ul>
  <v-checkbox :label="$t('I agree')" v-model="hasAgreedPriv" />

  <h2>{{$t('Covid19 rules')}}</h2>
  <div>See <a href="/page/covid19" target="_blank">Covid19</a></div>
  <v-checkbox :label="$t('I agree')" v-model="hasAgreedCovid" />  

  <div>
    <v-btn @click="next" v-show="agreed" color="primary">
      {{ $t('Continue') }}
    </v-btn>
    <v-btn @click="prev">{{$t('Back')}}</v-btn>
  </div>

</div>
</template>

<script>

import {mapState} from 'vuex'

export default {
  name: "SubscriptionNationality",

  data () {return {
    hasAgreedCovid: false ,
    hasAgreedNat: false,
    hasAgreedPriv: false,
  }},

  computed: {
    agreed () { 
      return this.hasAgreedNat && this.hasAgreedPriv && this.hasAgreedCovid
    },
    natstatus () {
      if (this.subscription.nationality == 'BEL') {
        if (this.subscription.idfide) {
          return 'fidebelg'
        }
        else {
          return 'maybe'
        }
      }
      else {
        if (this.subscription.idfide) {
          return 'nobelg'
        }
        else {
          return 'maybe'
        }
      }
    },    
    ...mapState(['flow', 'subscription', 'api'])
  },

  methods: {
    next () {
      this.$store.commit('updateFlow', {step: this.flow.step+1})
    },

    prev () {
      this.$store.commit('updateFlow', {step: this.flow.step-1})
    },
  },

}
</script>

<style scoped>

</style>