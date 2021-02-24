<template>
<div>
  <h2>Intro</h2>
  <div>
    {{ $t('You need your id number of the Royal Belgian Chess Federation in order to subscribe to the Belgian Chess Championships.') }}
  </div>
  <div class=mt-2>
  {{ $t('In case you do not have an id number of the RBCF, please contact your chess club, which can provide it.') }}</div>
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