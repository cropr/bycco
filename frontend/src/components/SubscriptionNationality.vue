<template>
<div>
  <h2>{{$t('Nationality')}}</h2>
  <div v-show="subscription.natstatus == 'fidebelg'">{{$t('SubNat1')}}</div>
  <div v-show="subscription.natstatus == 'nobelg'">{{$t('SubNat2')}}</div>
  <div v-show="subscription.natstatus == 'maybe'">{{$t('SubNat3')}}</div>
  <v-checkbox :label="$t('I agree')" v-model="hasAgreedNat"></v-checkbox>
  <h3>{{$t('Privacy rules')}}</h3>
  <div>{{$t('SubNat4')}}</div>
  <div>{{$t('SubNat5')}}</div>
  <ul>
    <li>{{$t('SubNat6')}}</li>
    <li>{{$t('SubNat7')}}</li>
    <li>{{$t('SubNat8')}}</li>
    <li>{{$t('SubNat9')}}</li>
    <li>{{$t('SubNat10')}}</li>
  </ul>
  <v-checkbox :label="$t('I agree')" v-model="hasAgreedPriv"></v-checkbox>
  <div>
    <v-btn @click="next" v-show="agreed" color="primary">{{$t('Continue')}}</v-btn>
    <v-btn @click="prev">{{$t('Back')}}</v-btn>
  </div>

</div>
</template>

<script>

import {mapState} from 'vuex'

export default {
  name: "SubscriptionNationality",

  computed: {
    hasAgreedNat: {
      get () {
        return this.flow.hasAgreedNat
      },
      set (value) {
        this.$store.commit('updateFlow', {hasAgreedNat: value})
      }
    },

    hasAgreedPriv: {
      get () {
        return this.flow.hasAgreedPriv
      },
      set (value) {
        this.$store.commit('updateFlow', {hasAgreedPriv: value})
      }
    },
    agreed () { return this.hasAgreedNat && this.hasAgreedPriv;},
    ...mapState(['flow', 'subscription'])
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