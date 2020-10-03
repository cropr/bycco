<template>
<v-container>
  <h1>Edit Page </h1>
  <v-card>
    <v-card-title color="grey lighten-4">
      {{ p.name }}
      <v-spacer />
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" outlined fab color="deep-purple" @click="back()" 
              slot="activator">
            <v-icon>mdi-arrow-left</v-icon>
          </v-btn>
        </template>
        <span>Go Back</span>
      </v-tooltip>
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" outlined fab color="deep-purple" @click="save()" 
              slot="activator">
            <v-icon>mdi-content-save</v-icon>
          </v-btn>
        </template>
        <span>Save page</span>
      </v-tooltip>
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" outlined fab color="deep-purple" @click="remove()" 
              slot="activator">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </template>
        <span>Delete page</span>
      </v-tooltip>
    </v-card-title>
    <v-card-text>
      <v-row>
        <v-col cols=12 sm=6>
          <v-text-field label="Name" v-model="p.name" />
          <v-text-field label="Owner" v-model="p.created_by" />
          <v-text-field label="Slug" v-model="p.slug" />
          <v-select :items="doctypes" label="Document type" v-model="p.doctype" />      
          <v-select :items="pagecomponents" label="Frontend Component" v-model="p.component" /> 
        </v-col>
        <v-col cols=12 sm=6>
          <v-checkbox v-model="p.enabled" label='Enabled' />
          <p>Page created: <date-formatted :date="p.creationtime"/></p>
          <p>Page modified: <date-formatted :date="p.modificationtime"/></p>
          <v-menu v-model="menu_published" :close-on-content-click="false"
            :nudge-right="40" transition="scale-transition"
            offset-y min-width="290px"
          >
            <template v-slot:activator="{ on }">
              <v-text-field v-model="p.publicationdate" label="Publication date" prepend-icon="mdi-calendar-range"
                readonly v-on="on" />
            </template>
            <v-date-picker v-model="p.publicationdate" @input="menu_published = false" color="deep-purple" />
          </v-menu>
          <v-menu v-model="menu_expired" :close-on-content-click="false"
            :nudge-right="40" transition="scale-transition"
            offset-y min-width="290px"
          >
            <template v-slot:activator="{ on }">
              <v-text-field v-model="p.expirationdate" label="Expiry date" prepend-icon="mdi-calendar-range"
                readonly v-on="on" />
            </template>
            <v-date-picker v-model="p.expirationdate" @input="menu_expired = false" color="deep-purple" />
          </v-menu>
        </v-col>
      </v-row>
      <h4>Translations</h4>
      <v-tabs class="elevation-2" >
        <v-tab v-for="l in languages" :key="l">
          {{ l }}
        </v-tab>
        <v-tab-item v-for="l in languages" :key="l">
          <v-checkbox v-model="enabled[l]" :label="l" class='pl-5' />
          <v-text-field class="mx-3" v-model='titles[l]' label="Title" />
          <v-text-field class="mx-3" v-model='intros[l]' label="Intro" />
          <v-textarea class="mx-3" solo v-model='bodys[l]' label="Body" />
        </v-tab-item>
      </v-tabs>   
    </v-card-text>
  </v-card>
</v-container>
</template>

<script>

import DateFormatted from "@/components/DateFormatted"
import { mapState } from 'vuex'
import { bearertoken } from "@/util/token"
import { doctypes, pagecomponents } from '@/util/cms'

export default {

  name: "PageEdit",

  components: {
    DateFormatted,
  },

  computed: {
    ...mapState(['token', 'api']),
    enabledLang: function(){
      let la = [], self=this;
      this.lang.available.forEach(function(l){
        if (self.lang.enabled[l] === true) {
          la.push(l)
        }
      })
      return la      
    },
  },

  data () {return {
    activetab: '',
    dialogDelete : false,
    doctypes: doctypes,    
    enabled: {en: false, nl: false, fr: false, de: false},
    languages: ['en', 'nl', 'fr', 'de'],
    idpage: this.$route.params.id,
    menu_published: false,
    menu_expired: false,
    p: {},
    pagecomponents: pagecomponents,
    intros: {en: '', nl: '',  fr: '', de: ''},
    titles: {en: '', nl: '',  fr: '', de: '', default: ''},
    bodys: {en: '', nl: '',  fr: '', de: ''},
  }},

  methods: {

    back () {
      this.$router.push('/mgmt/page/list');
    },

    getPage() {
      let self=this;
      this.api.get_page(
        {id: this.$route.params.id},
        {securities: bearertoken(this.token)},
      ).then(
        function(data) {
          self.readPage(data.obj);
        },
        function(data){
          console.error('failed get page', data)
          self.$root.$emit('snackbar', {text: 'Getting page failed', reason: data})          
        }
      );
    },

    publish() { },

    readPage(page) {
      let self=this, ls;
      this.p = {...page};
      this.enabled = {'en': false, 'nl': false, 'fr': false, 'de': false};
      ls = this.p.languages;
      this.activetab = ls[0];
      this.titles.default = this.p.title.default.value;
      this.languages.forEach(function(l){
          self.bodys[l] = self.p.body.default.value;
          self.titles[l] = self.p.title.default.value;
          self.intros[l] = self.p.intro.default.value;
      })
      ls.forEach(function(l){
          self.enabled[l] = true;
          self.bodys[l] = self.p.body[l] ? self.p.body[l].value: 
            self.p.bodys.default.value;
          self.titles[l] = self.p.title[l] ? self.p.title[l].value: 
            self.p.title.default.value;
          self.intros[l] = self.p.intro[l] ? self.p.intro[l].value: 
            self.p.intro.default.value;
      })
    },

    remove() {
      let self=this;
      if (window.confirm('Are you sure to delete page "' + this.name + '"?')) {
        this.api.delete_page(
          {id: this.$route.params.id },        
          {securities: bearertoken(this.token)}, 
        ).then(
          function(){
            self.$root.$emit('snackbar', {text: 'Page deleted'})
            self.back();
          }, 
          function(data){
            // TODO show error message
            console.error('failed to delete', data);
            self.$root.$emit('snackbar', {text: 'Delete page failed', reason: data})
          }
        );
      }
    },

    save () {
      var self = this, ls = [];
      this.languages.forEach(function(l){
        if (self.enabled[l]) {
          ls.push(l);
          if (!self.p.body[l]) {
            self.p.body[l] =  {...self.p.body.default}; 
          }
          self.p.body[l].value = self.bodys[l];
          if (!self.p.intro[l]) {
            self.p.intro[l] =  {...self.p.intro.default}; 
          }
          self.p.intro[l].value = self.intros[l];
          if (!self.p.title[l]) {
            self.p.title[l] =  {...self.p.title.default}; 
          }
          self.p.title[l].value = self.titles[l];
        }
        else {
          delete self.p.body[l]
          delete self.p.intro[l]
          delete self.p.title[l]
        }
      })
      this.api.update_page({id: this.idpage}, {
        requestBody: {
          body: this.p.body,
          component: this.p.component,
          doctype: this.p.doctype,
          enabled: this.p.enabled,
          expirationdate: this.p.expirationdate,
          intro: this.p.intro,
          languages: ls,
          name: this.p.name,
          owner: this.p.owner,
          publicationdate: this.p.publicationsdate,
          slug: this.p.slug,
          title: this.p.title,
        },
        securities: bearertoken(this.token),
      }).then(
        function () {
          self.$root.$emit('snackbar', {text: 'Page saved'})
          self.back();
        },
        function (data) {
          console.error('failed to delete', data);
          self.$root.$emit('snackbar', {text: 'Update page failed', reason: data})
        }
      )      
    },

    toggleLang(l){
      this.p.languages = this.enabledLang;
      if (l in this.p.page_i18n_fields === false) {
        this.p.page_i18n_fields[l] = {
          body: '',
          intro: '',
          title: '',
        }
      }
    },
  },

  mounted () {
    this.getPage();
  }

}
</script>

<style scoped>
.bordermd {
  border: 1px solid grey;
}
</style>