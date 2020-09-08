<template>
 <div>
  <v-parallax   v-if="$vuetify.breakpoint.mdAndUp" src="/img/pier_big.jpg" 
    height="400" />
  <v-parallax v-if="$vuetify.breakpoint.sm"
              src="/img/pier_medium.jpg" height="300" />
  <v-parallax v-if="$vuetify.breakpoint.xs"
              src="/img/pier_small.jpg" height="200" /> 
  <v-container class="mt-1">
    <h1 v-html="title" />
    <div v-html="intro" class="mt-1"/>
    <hr/>
    <div v-html="body" class="mt-1" />
    <v-row class="mt-2">
      <v-col cols=12 sm=6 md=4 v-for="art in articles" :key="art.id">
        <v-card>
          <v-card-title class="blue-grey lighten-1 black--text pa-3">
            {{ art.page_i18n_fields[locale].title }}
          </v-card-title>
          <v-card-text class="mt-2">
            {{ art.page_i18n_fields[locale].intro }}
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn @click="gotoArticle(art)">
              {{ $t('Read more') }}
            </v-btn>
          </v-card-actions>            
        </v-card>
      </v-col>
    </v-row>
  </v-container>
 </div>
</template>

<script>
import {mapState} from "vuex"
import marked from 'marked'
import { notitle, nointro } from "@/util/cms"

export default {

name: 'LandingPage',

data () {return {
  articles: [],
  page: {},
}},

computed: {
  body () { 
    return marked(this.page.body || '' )
  },
  intro () { 
    return marked(this.page.intro || '' )
  },
  title () { 
    return this.page.title || '' 
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
        self.page =  data.obj.page;
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

a {
  text-decoration: none;
}

a:hover {
  font-weight: bold;
}

</style>
