<template>
<v-container class="elevation-1">
  <v-row>
    <v-col cols=12 sm=6>
        <h1>Edit Document: {{d.name}} </h1>
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
        <span>Delete document</span>
      </v-tooltip>
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" outlined fab color="deep-purple" @click="saveDoc()" 
              slot="activator">
            <v-icon>save</v-icon>
          </v-btn>
        </template>
        <span>Save document</span>
      </v-tooltip>
      <v-tooltip bottom >
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" outlined fab color="deep-purple" @click="publishDoc()" 
              slot="activator">
            <v-icon>publish</v-icon>
          </v-btn>
        </template>
        <span>Publish document</span>
      </v-tooltip>
    </v-col>
  </v-row>
  <v-row>
    <v-col cols=12 sm=6>
      <v-text-field label="name" v-model="d.name" />
      <v-text-field label="Owner" v-model="d.owner" />
      <v-select :items="dt" v-model="d.doctype" label="Document type" />
      <p>Active: {{ d.active}} </p>      
    </v-col>
    <v-col cols=12 sm=6>
      <v-text-field label="Slug" v-model="d.slug" />
      <v-text-field label="Languages" v-model="lang" />
      <p>Document created: <date-formatted :date="d.creationtime"/></p>
      <p>Document modified: <date-formatted :date="d.modificationtime"/></p>
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
import {doctypes, languages, yesno} from '@/util/const'

export default {

  name: "DocEdit",

  components: {
    DateFormatted,
  },

  data () {return {
    intro: {nl:'', fr:'', en:'', de: ''},
    content: {nl:'', fr:'', en:'', de: ''},
    title: {nl:'', fr:'', en:'', de: ''},
    currentLang: 'nl',
    langix: 0,
    lang: '',
    languages: languages,
    d: {},
    dt: [],
    yesno: yesno, 
  }},

  methods: {

    back () {
      this.$router.back();
    },

    publishDoc() {
      this.d.publishedtime = new Date();
      this.saveDoc();
    },

    readDoc (doc) {
      this.d = doc;
      languages.forEach(function(l) {
        if (doc.i18n_fields[l]) {
          this.content[l] = doc.i18n_fields[l].content;
          this.intro[l] = doc.i18n_fields[l].intro;
          this.title[l] = doc.i18n_fields[l].title;
        }
        else {
          this.content[l] = '';
          this.intro[l] = '';
          this.title[l] = '';
        } 
      }.bind(this))
      this.lang = doc.languages.join(',')
      console.log('lang', this.lang)
    },

    remove () {
      if (window.confirm('Are you sure to delete ' + this.fullname)) {
        api('deleteAttendee', {
          id: this.participant.id
        }).then(function(){
          this.$emit('snackbar', {text: 'Document deleted.'})
          this.$router.push('/mgmt/doc/list')
        }.bind(this), function(data){
          this.$emit('snackbar', {text: ' failed to delete.' + data})
        })
      }
    },

    saveDoc () {
      let doc = this.d;
      this.languages.forEach(function(l) {
        doc.i18n_fields[l] = {
          title: this.title[l],
          intro: this.intro[l],
          content: this.content[l],
        }
      }.bind(this));
      doc.languages = this.lang.split(',');
      api('updateDoc', {
        id: this.d.id,
        document: doc,
      }).then(
        function(data){
          this.readDoc(data.document)
          this.$emit('snackbar', {text: 'Document saved.'})
        }.bind(this),
        function(data){
          this.$emit('snackbar', {text: ' failed to save.' + data})
        }
      );
    },

  },

  mounted () {
    doctypes.forEach(function(v){
      this.dt.push({value: v[0], text:v[1]})
    }.bind(this))
    api('getDoc', {
      id: this.$route.params.id
    }).then(
     function(data) {
       this.readDoc(data.document)
      }.bind(this)
    ),
    function(data){
      console.error('failed get doc', data)
    }
  }

}
</script>

<style scoped>
.bordermd {
  border: 1px solid grey;
}
</style>