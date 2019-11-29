<template>
<v-container class="elevation-1">
  <v-row>
    <v-col cols=12 sm=6>
        <h1>Edit Page: {{p.name}} </h1>
    </v-col>
    <v-col col=12 sm=6>
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" outlined fab color="deep-purple" @click="back()" 
              slot="activator">
            <v-icon>arrow_back</v-icon>
          </v-btn>
        </template>
        <span>Go Back</span>
      </v-tooltip>
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" outlined fab color="deep-purple" @click="remove()" 
              slot="activator">
            <v-icon>delete</v-icon>
          </v-btn>
        </template>
        <span>Delete page</span>
      </v-tooltip>
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" outlined fab color="deep-purple" @click="save()" 
              slot="activator">
            <v-icon>save</v-icon>
          </v-btn>
        </template>
        <span>Save page</span>
      </v-tooltip>
      <v-tooltip bottom >
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" outlined fab color="deep-purple" @click="publish()" 
              slot="activator">
            <v-icon>publish</v-icon>
          </v-btn>
        </template>
        <span>Publish page</span>
      </v-tooltip>
      <v-tooltip bottom >
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" outlined fab color="deep-purple" @click="preview()" 
              slot="activator">
            <v-icon>visibility</v-icon>
          </v-btn>
        </template>
        <span>Preview page</span>
      </v-tooltip>
    </v-col>
  </v-row>
  <v-row>
    <v-col cols=12 sm=6>
      <v-text-field label="name" v-model="p.name" />
      <v-text-field label="Owner" v-model="p.owner" />
      <v-text-field label="Template" v-model="p.template" />
    </v-col>
    <v-col cols=12 sm=6>
      <v-text-field label="Slug" v-model="p.slug" />
      <v-text-field label="Languages" v-model="lang" />
      <p>Page created: <date-formatted :date="p.creationtime"/></p>
      <p>Page modified: <date-formatted :date="p.modificationtime"/></p>
    </v-col>
  </v-row>
  <v-tabs light slider-color="deep-purple" v-model="langix" >
    <v-tab class="mx-2"  v-for="l in languages" :key="l">
      <span>{{l}}</span>
    </v-tab>
  </v-tabs>
  <v-tabs-items v-model="langix">
    <v-tab-item  v-for="l in languages" :key="l">
      <div class='elevation-1 mt-2 pa-2'>
        <v-text-field label="Title" v-model="title[l]" />
        <v-textarea auto-grow rows=3 label="Intro" 
          v-model="intro[l]" /> 
        <v-textarea auto-grow rows=8 label="Content" 
          v-model="content[l]" /> 
      </div>
    </v-tab-item>
  </v-tabs-items>

</v-container>
</template>

<script>

import api from '@/util/api'
import DateFormatted from "@/components/DateFormatted"

export default {

  name: "PageEdit",

  components: {
    DateFormatted,
  },

  data () {return {
    content: {nl:'', fr:'', en:'', de: ''},
    currentLang: 'nl',
    intro: {nl:'', fr:'', en:'', de: ''},
    languages: ['nl', 'fr', 'de', 'en'],
    langix: 0,
    lang: '',
    title: {nl:'', fr:'', en:'', de: ''},
    p: {},
    yesno: [
      {value:true, text: 'Yes'},
      {value:false ,text:'No'}
    ],
  }},

  methods: {

    back () {
      this.$router.back();
    },

    preview () {

    },

    publish() {

    },

    readPage (page) {
      this.p = page;
      this.languages.forEach(function(l) {
        if (page.i18n_fieldset[l]) {
          this.content[l] = page.i18n_fieldset[l].content;
          this.intro[l] = page.i18n_fieldset[l].intro;
          this.title[l] = page.i18n_fieldset[l].title;
        }
        else {
          this.content[l] = '';
          this.intro[l] = '';
          this.title[l] = '';
        } 
      }.bind(this))
      this.lang = page.languages.join(',')
    },

    remove () {
      if (window.confirm('Are you sure to delete ' + this.fullname)) {
        api('deleteAttendee', {
          id: this.participant.id
        }).then(function(){
          this.$emit('update', {section: 'list', params:{}, reload: true,
            text: this.fullname + ' deleted.'})
        }.bind(this), function(data){
          console.error('failed to delete', data);
        })
      }
    },

    save () {
      let page = this.p;
      this.languages.forEach(function(l) {
        page.i18n_fieldset[l] = {
          title: this.title[l],
          intro: this.intro[l],
          content: this.content[l],
        }
      }.bind(this));
      page.languages = this.lang.split(',');
      api('updatePage', {
        id: this.p.id,
        page: page,
      }).then(
        function(){
          this.$router.push('/mgmt/page/list')
        }.bind(this),
        function(data){
          console.error('failed to save', data);
        }
      );
    },

  },

  mounted () {
    api('getPageById', {
      id: this.$route.params.id
    }).then(
     function(data) {
       this.readPage(data.page)
      }.bind(this)
    ),
    function(data){
      console.error('failed get page', data)
    }
  }

}
</script>

<style scoped>
.bordermd {
  border: 1px solid grey;
}
</style>