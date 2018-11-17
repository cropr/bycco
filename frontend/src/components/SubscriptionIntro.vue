<template>
<div>
  <h2>Intro</h2>
  <div v-t="'SubIntro1'"></div>
  <ul>
    <li v-t="'SubIntro2'"></li>
    <li v-t="'A photo for your badge'"></li>
  </ul>
  <div v-t="'SubIntro3'"></div>
  <div v-t="'SubIntro4'"></div>
  <v-btn v-t="'Continue'" @click="next" color="primary"></v-btn>
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