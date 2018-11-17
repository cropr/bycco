<template>
<div>
  <h2 v-t="'Nationality'"></h2>
  <div v-show="subscription.natstatus == 'fidebelg'" v-t="'SubNat1'"></div>
  <div v-show="subscription.natstatus == 'nobelg'" v-t="'SubNat2'"></div>
  <div v-show="subscription.natstatus == 'maybe'" v-t="'SubNat3'"></div>
  <v-checkbox :label="$t('I agree')" v-model="hasAgreedNat"></v-checkbox>
  <h3 v-t="'Privacy rules'"></h3>
  <div v-t="'SubNat4'"></div>
  <div v-t="'SubNat5'"></div>
  <ul>
    <li v-t="'SubNat6'"></li>
    <li v-t="'SubNat7'"></li>
    <li v-t="'SubNat8'"></li>
    <li v-t="'SubNat9'"></li>
    <li v-t="'SubNat10'"></li>
  </ul>
  <v-checkbox :label="$t('I agree')" v-model="hasAgreedPriv"></v-checkbox>
  <div>
    <v-btn v-t="'Continue'" @click="next" v-show="agreed" color="primary"></v-btn>
    <v-btn v-t="'Back'" @click="prev"></v-btn>
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