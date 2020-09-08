<template>

<v-container>
  <h1>Management Pages</h1>
  <v-data-table :headers="headers" :items="filteredpages" :footer-props="footerProps"
      class="elevation-1" :sort-by="['name','modified']">
    <template v-slot:top>
      <v-toolbar flat color="white">
        <v-toolbar-title>
          Pages
        </v-toolbar-title>
        <v-spacer />
        <v-row>
          <v-col cols=3>
            <v-checkbox v-model="filter.normal" label='page' />
          </v-col>
          <v-col cols=3>
            <v-checkbox v-model="filter.article" label='article' />&nbsp;&nbsp;
          </v-col>
          <v-col cols=3>
            <v-checkbox v-model="filter.app" label='app' />
          </v-col>
        </v-row>
        <v-spacer />
        <v-tooltip bottom >
          <template v-slot:activator="{ on }">
            <v-btn v-on="on" @click="addPage()" fab outlined 
                  color="deep-purple">
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </template>
          <span>Add Page</span>
         </v-tooltip>
      </v-toolbar>
    </template>
    <template v-slot:item.modified_ts="{ item }">
      <date-formatted :date="item.modified_ts"/>
    </template>
    <template v-slot:item.action="{ item }">
      <v-icon small class="mr-2"  @click="editPage(item)" >
        mdi-pencil
      </v-icon>
    </template>
    <template v-slot:no-data>
      No pages found.
    </template>            
  </v-data-table>
</v-container>

</template>

<script>

import { mapState } from 'vuex'
import { bearertoken } from "@/util/token"
import DateFormatted from "@/components/DateFormatted"


export default {

  name: 'PageList',

  data () {return {
    filter: {},
    footerProps: {
      itemsPerPageOptions: [20,50,-1],
      itemsPerPage: 20,
    },
    headers: [
      {
        text: "Name", value: 'name'
      },
      {
        text: "Doctype", value: 'doctype'
      },
      {
        text: "Enabled", value: 'enabled'
      },
      {
        text: "Modified", value: 'modified_ts'
      },
      {
        text: 'Actions', value: 'action', sortable: false
      }
    ],    
    pages: [],
  }},

  computed: {
    ...mapState(['token', 'api']),
    filteredpages: function() {
      let self=this, pa=[]
      if (!this.filter.normal && !this.filter.article && !this.filter.app)
        return this.pages;
      this.pages.forEach(function(p){
        if (p.doctype == 'normal-page' && self.filter.normal) {
          pa.push(p);
          return
        }
        if (p.doctype == 'article' && self.filter.article) {
          pa.push(p);
          return
        }
        if (p.doctype == 'app-page' && self.filter.app) {
          pa.push(p);
          return
        }
      })
      return pa 
    },
  },

  components: {
    DateFormatted,
  },

  methods: {

    addPage () {
      this.$router.push('/mgmt/page/add')
    },

    editPage (item) {
      this.$router.push('/mgmt/page/edit/'  + item.id)
    },
    
    getPages() {
      let self=this;
      console.log('getPages bearer', bearertoken(this.token))
      this.api.get_pages(
        {},
        {securities: bearertoken(this.token)},
      ).then(
        function(data) {
          self.pages = data.obj.pages;
          self.pages.forEach(function(p){
            p.created_ts = (new Date(p.created_ts)).toLocaleString();
            p.modified_ts = (new Date(p.modified_ts)).toLocaleString();
          })
        },
        function(data){
          if (data.status == 401) {
            self.$router.push('/mgmt/login')
          }
          else {
            console.error('getting getPages', data);
            self.$root.$emit('snackbar', {text: 'Getting pages failed', reason: data})            
          }
        }
      );
    }
    
  },

  mounted () {
    this.getPages();
  },  

}
</script>
