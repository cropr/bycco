<template>
<div>
  <h2>{{ $t(intro1) }} </h2>
  <div  class=mt-2>
    {{ $t(intro2) }}
    <ul>
      <li>{{ $t(intro3) }}</li>
      <li>{{ $t(intro4) }}</li>
      <li>{{ $t(intro5) }}</li>
      <li>{{ $t(intro6) }}</li>
      <li>{{ $t(intro7) }}</li>
    </ul>
  </div>
  <div class=mt-2>
    <v-btn @click="next" color="primary">{{$t('Continue')}}</v-btn>
  </div>
</div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  name: "LodgingIntro",
  data () {return {
    intro1: `Lodging reservation`,
    intro2: `In order to make a reservation you need to provide the following elements:`,
    intro3: `which type of accomodation you want`,
    intro4: `start date and end date`,
    intro5: `the name, firat name, birth date of every person`,
    intro6: `which persons are participants to the tournament`,
    intro7: `the meals you want`,
  }},
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
