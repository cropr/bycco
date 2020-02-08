<template>

  <v-container class="mt-1 markedcontent">
    <h1>{{ doc.i18n_fields.title }}</h1>
    <v-row>
      <v-col cols="12" sm="6" md="4" v-for="(slug,ix) in subpages" :key="ix">
        <v-card>
          <v-card-title class="blue-grey white--text">{{ titles[slug] }}</v-card-title>
          <v-card-text class=mt-2 v-html="content[slug]"></v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>

</template>

<script>
import Vue from 'vue'

import api from '@/util/api'
import {mapState} from "vuex"
import marked from 'marked'


export default {

  name: 'DocAgenda',

  data () {return {
    titles: {},
    content: {},
    subpages: [],
  }},

  computed: {
    ...mapState(['doc', 'locale']),
  },

  watch: {
    doc () {
      this.subpages = this.doc.i18n_fields.content.split('\n');
      this.subpages.forEach(function(slug) {
        Vue.set(this.titles, slug, '');
        Vue.set(this.content, slug, '');
        api('getDoc', {
          idtype: 'slug',
          id: slug,
          locale: this.locale,
        }).then(function(data) {
          this.titles[slug] = data.document.i18n_fields.title;
          this.content[slug] = marked(data.document.i18n_fields.content || '');
        }.bind(this), function(data) {
          console.error('error loading doc', data);
        })
      }.bind(this));

    }
  },

}
</script>


<style>

</style>
