<template>

  <v-container class="mt-1 markedcontent" v-html="content" />

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
    ...mapState(['doc']),
    content () {
      if (!this.doc) return '';
      if (!this.doc.i18n_fields) return '';
      return marked(this.doc.i18n_fields.content || '')
    },
  },

  mounted () {
  },

}
</script>


<style>

.markedcontent table {
border-collapse: collapse;
min-width: 30em;
}

.markedcontent table {
  border: 1px solid black;
}

.markedcontent td {
  border: 1px solid black;
  padding: 6px;
}

.markedcontent  th {
  border: 1px solid black;
  padding: 6px;
}

</style>
