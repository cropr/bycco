<template>
<v-container fluid grid-list-md class="elevation-1">
  <v-layout row wrap>
    <v-flex>
        <h1>Edit Article: {{p.maintitle}} </h1>
    </v-flex>
    <v-flex>
      <v-tooltip bottom>
        <v-btn outline fab color="green" @click="back()" slot="activator">
          <v-icon>arrow_back</v-icon>
        </v-btn>
        <span>Go Back</span>
      </v-tooltip>
      <v-tooltip bottom>
        <v-btn outline fab color="green" @click="remove()" slot="activator">
          <v-icon>delete</v-icon>
        </v-btn>
        <span>Delete participant</span>
      </v-tooltip>
      <v-tooltip bottom>
        <v-btn outline fab color="green" @click="save()" slot="activator">
          <v-icon>save</v-icon>
        </v-btn>
        <span>Save changes</span>
      </v-tooltip>
      <v-tooltip bottom v-show="p.status != 'published'">
        <v-btn outline fab color="green" @click="publishnow()" slot="activator">
          <v-icon>publish</v-icon>
        </v-btn>
        <span>Publish now</span>
      </v-tooltip>
      <v-tooltip bottom v-show="p.status == 'published'">
        <v-btn outline fab color="green" @click="archivenow()" slot="activator">
          <v-icon>archive</v-icon>
        </v-btn>
        <span>Archive now</span>
      </v-tooltip>
    </v-flex>
  </v-layout>
  <v-layout row wrap>
    <v-flex sm6 xs12>
      <v-text-field label="Author" v-model="p.author" />
      <p>Article created: <date-formatted :date="p.created"/></p>
      <p>Article last modified: <date-formatted :date="p.modified"/></p>
      <v-menu :close-on-content-click="false" v-model="menu_startdate"
        :nudge-right="40" lazy transition="scale-transition" offset-y
        full-width min-width="290px">
        <v-text-field slot="activator" v-model="p.startdate"
          label="Start date publication" prepend-icon="event" readonly
        ></v-text-field>
        <v-date-picker v-model="p.startdate" @input="menu_startdate = false"
                       color="green" />
      </v-menu>
      <v-menu :close-on-content-click="false" v-model="menu_enddate"
        :nudge-right="40" lazy transition="scale-transition" offset-y
        full-width min-width="290px">
        <v-text-field slot="activator" v-model="p.enddate"
          label="End date publication" prepend-icon="event" readonly
        ></v-text-field>
        <v-date-picker v-model="p.enddate" @input="menu_enddate = false"
                       color="green" />
      </v-menu>
    </v-flex>
    <v-flex sm6 xs12>
      <v-text-field label="Slug" v-model="p.slug" />
      <v-select label="Main locale" v-model="p.mainlocale" :items="languages" />      
      <v-select label="Show 'read more'" v-model="p.readmore" :items="yesno" />  
    </v-flex>
  </v-layout>
  <v-tabs light slider-color="pink" v-model="langix" @change="setLanguage">
    <v-tab class="mx-2"  v-for="l in languages" :key="l">
      <span>{{l}}</span>
    </v-tab>
  </v-tabs>
  <v-tabs-items v-model="langix">
    <v-tab-item  v-for="l in languages" :key="l">
      <v-layout class='elevation-1 mt-2 pa-2' row wrap>
        <v-flex sm6>
          <v-text-field label="Title" v-model="p[l].title" />
        </v-flex>
        <v-flex sm6/>
        <v-flex sm6>
          <v-textarea auto-grow box rows=3 label="Intro" v-model="p[l].intro" 
            @input="introWrapper" /> 
        </v-flex>
        <v-flex sm6>
          <div class="pa-2 elevation-1" v-html="compiledIntro"></div>
        </v-flex>
        <v-flex sm6>
          <v-textarea auto-grow box rows=5 label="Content" v-model="p[l].content" 
            @input="contentWrapper" /> 
        </v-flex>
        <v-flex sm6>
          <div class="pa-2 bordermd" v-html="compiledContent"></div>
        </v-flex>
      </v-layout>
    </v-tab-item>
  </v-tabs-items>


</v-container>
</template>

<script>

import api from '../util/api'
import _ from 'lodash'
import marked from 'marked'

import DateFormatted from "@/components/DateFormatted"

export default {

  name: "PagePreview",

  components: {
    DateFormatted,
  },

  props: ['article'],

  computed :  {
    fullname () {
      return this.p.first_name + ' ' + this.p.last_name;
    },
  },

  data () {return {
    compiledIntro: '',
    compiledContent: '',
    languages: ['nl', 'fr', 'de', 'en'],
    langix: 0,
    currentLang: 'nl',
    menu_enddate: false,
    menu_startdate: false,
    p: {en:{}, de:{}, fr:{}, nl:{}},
    snacktext: '',
    statusus: ['created', 'published', 'archived'],
    yesno: [
      {value:true, text: 'Yes'},
      {value:false ,text:'No'}
    ],
    contentWrapper: null,
    introWrapper: null, 
  }},

  methods: {

    back () {
      this.$emit('update', {section: 'list'})
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
      this.p.published = this.p.startdate;
      this.p.archived = this.p.enddate;
      api('updateArticle', {
        id: this.article.id,
        article: this.p,
      }).then(
        function(){
          this.$emit('update', {section: 'edit' , reload: true,
            text: this.p.maintitle + ' saved.'})
        }.bind(this),
        function(data){
          console.error('failed to save', data);
        }
      );
    },

    setLanguage () {
      this.currentLang = this.languages[this.langix];
      this.contentWrapper = function(e){
        _.debounce(function(){
          this.p[this.currentLang].content = e;
          this.compiledContent = marked(e, {sanitize: true})
        }.bind(this))()
      }.bind(this);
      this.introWrapper = function(e){
        _.debounce(function(){
          this.p[this.currentLang].intro = e;
          this.compiledIntro = marked(e, {sanitize: true})
        }.bind(this))()
      }.bind(this);
      this.compiledContent = marked(this.p[this.currentLang].content);
      this.compiledIntro = marked(this.p[this.currentLang].intro);
    },

    updateIntro (l) {
      _.debounce(function(e){
          this.p.intro[l] = e.target.value;
          this.compiledIntro = marked(e.target.value, {sanitize: true})
        }.bind(this))
    },

  },

  mounted () {
    api('getArticle', {
      id: this.article.id
    }).then(
     function(data) {
        this.p = data.article;
        this.p.en = this.p.en || {};
        this.p.nl = this.p.nl || {};
        this.p.fr = this.p.fr || {};
        this.p.de = this.p.de || {};
        this.p.enddate = this.p.archived ? this.p.archived.split(
          ' ')[0] : '';
        this.p.startdate = this.p.published? this.p.published.split(
          ' ')[0]: '';
        this.setLanguage();        
      }.bind(this)
    )
  }

}
</script>

<style scoped>
.bordermd {
  border: 1px solid grey;
}
</style>