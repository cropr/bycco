<template>

  <v-container class="mt-1 markedcontent">
    <h1 v-html="title" />
    <div v-html="intro" class="mt-1 markdown-body"/>
    <hr/>
    <div v-html="body" class="mt-1 markdown-body" />
  </v-container>

</template>

<script>
import {mapState} from "vuex"
import marked from 'marked'

export default {

  name: 'CmsSimplePage',

  data () {return {
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
    
    getContent () {
    let self=this;
    this.api.anon_slug_page({
      slug: this.slug,
    }).then(
      function(data){
        self.page =  data.obj;
      },
      function(data){
        console.error('could not fetch localized page', data)
      }
    )
    },

  },

  mounted () {
    console.log('CmsSimplePage Mounted', this.slug)
    this.getContent();
  },

}
</script>


<style scoped>

</style>
