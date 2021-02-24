<template>
 <div class="mb-2">
  <v-parallax  v-if="$vuetify.breakpoint.mdAndUp" src="/img/pier_big.jpg" 
    height="400" />
  <v-parallax v-if="$vuetify.breakpoint.sm"
              src="/img/pier_medium.jpg" height="300" />
  <v-parallax v-if="$vuetify.breakpoint.xs"
              src="/img/pier_small.jpg" height="200" /> 
  <v-container class="mt-1">

  </v-container>
  <v-parallax  v-if="$vuetify.breakpoint.smAndUp"
    src="/img/winnaars_big.jpg" height="400" />
  <v-parallax v-if="$vuetify.breakpoint.xs"
    src="/img/winnaars_small.jpg" height="200" />  
 </div>
</template>

<script>
import { mapState } from "vuex"
import marked from 'marked'
import { notitle, nointro } from "@/util/server_injected"


export default {

  name: 'LandingPage',

  data () {return {
    articles: [],
    page: {},
  }},

  computed: {
    body () { 
      let pt = '';
      if (this.page.body) {
        pt = this.page.body.default.value;
        if (this.page.body[this.locale]) 
          pt = this.page.body[this.locale].value;
      }
      return marked(pt);
    },
    intro () { 
      let pt = '';
      if (this.page.intro) {
        pt = this.page.intro.default.value;
        if (this.page.intro[this.locale]) 
          pt = this.page.intro[this.locale].value;
      }
      return marked(pt);
    },
    title () {
      let pt = '';
      if (this.page.title) {
        pt = this.page.title.default.value;
        if (this.page.title[this.locale]) 
          pt = this.page.title[this.locale].value;
      }
      return pt;
    },
    ...mapState(['api', 'locale', 'slug']),

  },

  methods: {
    
    getActiveArticles () {
      let self=this;
      this.api.get_activearticles().then(
        function(data){
          self.readArticles(data.obj.articles);
        },
        function(data){
          console.error('could not fetch articles', data)
        }
      );
    },

    getContent () {
      let self=this;
      console.log('trying to get pages')
      this.api.anon_slug_page({
        slug: this.slug,
      }).then(
        function(data){
          self.page =  data.obj;
        },
        function(data){
          console.error('could not fetch localized page', data)
        }
      );
    },

    gotoArticle(art) {
      this.$router.push('/page/' +  art.slug + '/' + this.locale)
    },

    readArticles(art) {
      let self=this;
      this.articles3 = [];
      this.articleRest = [];
      art.forEach(function (a, index) {
        if (self.locale in a.page_i18n_fields === false) {
          a.page_i18n_fields[self.locale] = {
            title: '',
            intro: '',
            body: ''
          }
        }
        if (!a.page_i18n_fields[self.locale].title)
          a.page_i18n_fields[self.locale].title = notitle[self.locale];
        if (!a.page_i18n_fields[self.locale].intro)
          a.page_i18n_fields[self.locale].intro = nointro[self.locale];
        if (index < 3) {
          self.articles3.push(a);
        }
        else {
          self.articlesRest.push(a);
        }
      })
        
    },

  },

  mounted () {
    console.log('LandingPage Mounted', this.slug)
    this.getContent();
    // this.getActiveArticles();
  },

}
</script>


<style>

</style>
