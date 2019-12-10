<template>
<div>
  <h2>Intro</h2>
  <div>{{ $t('SubIntro1') }}:</div>
  <ul>
    <li>{{$t('SubIntro2')}}</li>
    <li>{{$t('A photo for your badge')}}</li>
  </ul>
  <div class=mt-2>{{$t('SubIntro4')}}</div>
  <div class=mt-2>
    <v-btn @click="next" color="primary">{{$t('Continue')}}</v-btn>
  </div>
</div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: "SubscriptionIntro",

  computed: {
      ...mapState(['flow'])
  },

  methods: {
    next () {
      this.$store.commit('updateFlow', {step: this.flow.step+1})
    }
  }
}
</script>

<style scoped>

</style>