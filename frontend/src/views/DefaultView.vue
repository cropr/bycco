<template>

  <v-container class="mt-1" v-html="content" />

</template>

<script>
import {mapState} from "vuex"
import marked from 'marked'


export default {

  name: 'DefaultView',

  data () {return {
    articles: []
  }},

  computed: {
    ...mapState(['page']),
    content () {
      return marked(this.page.i18n_content || '')
    },
  },

  mounted () {
  },

}
</script>


<style scoped>

.nopadding {
  padding-top: 0px !important;
}

</style>
