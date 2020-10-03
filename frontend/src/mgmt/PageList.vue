<template>

<v-container>
  <h1>Management Pages</h1>
  <v-data-table :headers="headers" :items="filteredpages" :footer-props="footerProps"
      class="elevation-1" :sort-by="['name','modified']">
    <template v-slot:top>
      <v-card color="grey lighten-4">
        <v-card-title>
          <v-row class="px-2">
            <v-checkbox v-model="filter.normal" label='page' />
            <v-spacer />
            <v-checkbox v-model="filter.article" label='article' />
            <v-spacer />
            <v-checkbox v-model="filter.app" label='app' />
            <v-spacer />
            <v-tooltip bottom >
              <template v-slot:activator="{ on }">
                <v-btn v-on="on" @click="addPage()" fab outlined 
                      color="deep-purple">
                  <v-icon>mdi-plus</v-icon>
                </v-btn>
              </template>
              Add Page
            </v-tooltip>
            <v-tooltip bottom >
              <template v-slot:activator="{ on }">
                <v-btn v-on="on" @click="backupPages()" fab outlined 
                      color="deep-purple">
                  <v-icon>mdi-download-multiple</v-icon>
                </v-btn>
              </template>
              Backup Pages
            </v-tooltip>          
          </v-row>
        </v-card-title>
      </v-card>
    </template>
    <template v-slot:item.modificationtime="{ item }">
      <date-formatted :date="item.modificationtime"/>
    </template>
    <template v-slot:item.action="{ item }">
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-icon v-on="on" small class="mr-2"  @click="editPage(item)" >
            mdi-pencil
          </v-icon>
        </template>
        Edit Page
      </v-tooltip>
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
        text: "Modified", value: 'modificationtime'
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

    backupPages () {
      let self=this;
      this.api.backup_pages(
        {},
        {securities: bearertoken(this.token)},
      ).then(
        function(data) {
          let link = document.createElement("a");
          let today= (new Date()).toISOString().substr(0,10);
          link.download = `pages_${today}.json`;
          link.href = 'data:,' + encodeURIComponent(data.text);
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
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

    },


    editPage (item) {
      this.$router.push('/mgmt/page/edit/'  + item.id)
    },
    
    getPages() {
      let self=this;
      this.api.get_pages(
        {},
        {securities: bearertoken(this.token)},
      ).then(
        function(data) {
          self.pages = data.obj.pages;
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
