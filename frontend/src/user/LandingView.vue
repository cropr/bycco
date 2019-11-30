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

    <!-- <h2>{{ $t('News items')}}</h2>
    <v-row>
      <v-col cols=12 sm=6 md=4 v-for="a in articles" :key="a.id">
        <v-card tile>
          <v-card-title class="blue-grey lighten-2 subtitle-2">
            {{a.title}}
          </v-card-title>
          <v-card-text class="mt-2">
            <div>{{a.intro}}</div>
          </v-card-text>
          <v-card-actions>
            <v-spacer/>
            <v-btn text class="blue-grey--text">{{ $t('Read More') }}</v-btn>
          </v-card-actions>  
        </v-card>
      </v-col>
    </v-row> -->

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
      if (!this.page.i18n_fields) return '';
      return marked(this.page.i18n_fields.title || '')
    },
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
/* .img-responsive {
  max-width: 100%;
} */
</style>
