<template>

  <v-container class="mt-1 markedcontent">
  <v-tabs light slider-color="deep-purple" v-model="lang" >
    <v-tab class="mx-2"  v-for="l in languages" :key="l">
      <span>{{l}}</span>
    </v-tab>
  </v-tabs>
  <v-tabs-items v-model="lang">
    <v-tab-item  v-for="l in languages" :key="l">
      <div class='elevation-1 mt-2 pa-2'>
        <h1 v-html="title[l]" />
        <div v-html="intro[l]" class="mt-1"/>
        <hr/>
        <div v-html="body[l]" class="mt-1" />
      </div>
    </v-tab-item>
  </v-tabs-items>      

  </v-container>

</template>

<script>
import {mapState} from "vuex"
import marked from 'marked'

export default {

  name: 'MultiLocalePage',

  data () {return {
    p: {},
    body: {},
    intro: {},
    title: {},
    languages: [],
    lang: '',
  }},

  computed: {

    ...mapState(['api', 'locale', 'slug']),

  },

  methods: {
    
    getContent () {
      let self=this;
      this.api.get_page_by_slug({
        slug: this.slug,
      }).then(
        function(data){
          self.readPage(data.obj.page);
        },
        function(data){
          console.error('could not fetch localized page', data)
        }
      );
    },

    readPage (page) {
      let self=this, localecontent;
      this.p = page;
      this.languages = []
      this.p.languages.forEach(function(l){
        if (l in self.p.page_i18n_fields) {
          localecontent = self.p.page_i18n_fields[l];
          self.body[l] = marked(localecontent.body || '');
          self.intro[l] = marked(localecontent.intro || '');
          self.title[l] = localecontent.title || '';
          if ( self.body[l] || self.intro[l] || self.title[l] ) {
            self.languages.push(l)
          }
        }
      })
      this.lang = this.languages[0];
    },    

  },

  mounted () {
    this.getContent();
  },

  watch: {
    locale: function (nv, ov) {
      console.log('watch locale', nv, ov)
      this.$router.push('/page/' + this.slug + '/' + nv)
    },
    slug: function (nv, ov) {
      console.log('watch slug', nv, ov)
      this.$router.push('/page/' + nv + '/' + this.locale)
    },
  }

}
</script>


<style scoped>

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
