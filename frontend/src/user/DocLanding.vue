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

  name: 'DocLanding',

  computed: {
    ...mapState(['doc']),
    title () {
      console.log('check 401')
      if (!this.doc) return '';
      console.log('check 402')
      if (!this.doc.i18n_fields) return '';
      return marked(this.doc.i18n_fields.title || '')
    },
    content () {
      console.log('check 403', this.doc)
      if (!this.doc) return '';
      console.log('check 404')
      if (!this.doc.i18n_fields) return '';
      return marked(this.doc.i18n_fields.content || '')
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
