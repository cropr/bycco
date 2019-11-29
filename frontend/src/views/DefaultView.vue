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
      if (!this.page) return '';
      if (!this.page.i18n_fields) return '';
      return marked(this.page.i18n_fields.content || '')
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
