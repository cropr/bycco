<template>

<div>

  <v-parallax   v-if="$vuetify.breakpoint.mdAndUp" src="/static/img/pier_big.jpg" 
    height="400" />
  <v-parallax v-if="$vuetify.breakpoint.sm"
              src="/static/img/pier_medium.jpg" height="300" />
  <v-parallax v-if="$vuetify.breakpoint.xs"
              src="/static/img/pier_small.jpg" height="200" />
              
  <v-container class="mt-1" v-html="content">
  </v-container>  

  <v-parallax  v-if="$vuetify.breakpoint.smAndUp"
    src="/static/img/winnaars_big.jpg" height="400" />
  <v-parallax v-if="$vuetify.breakpoint.xs"
    src="/static/img/winnaars_small.jpg" height="200" />

  <v-container class="mt-3 mb-2">

  </v-container>

</div>

</template>

<script>
import {mapState} from "vuex"
import marked from 'marked'


export default {

  name: 'LandingView',

  data () {return {
    articles: []
  }},

  computed: {
    ...mapState(['page']),
    title () {
      if (!this.page) return '';
      if (!this.page.i18n_fieldset) return '';
      return marked(this.page.i18n_fieldset.title || '')
    },
    content () {
      if (!this.page) return '';
      if (!this.page.i18n_fieldset) return '';
      return marked(this.page.i18n_fieldset.content || '')
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
/* .img-responsive {
  max-width: 100%;
} */
</style>
