<template>
  <span>{{ dateformatted }}</span>
</template>

<script>
import * as moment from 'moment';

import 'moment/locale/en-gb'

moment.locale('en-gb');

export default {
  name: "DateFormatted",
  props: ["date"],
  computed: {
    dateformatted () {
      return this.date ? moment(this.date).format('lll'): '';
    }
  }
}
</script>

<style scoped>

</style>