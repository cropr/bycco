<template>

<v-container>
  <h1>Management Documents</h1>
  <v-data-table :headers="headers" :items="docs" :footer-props="footerprops"
      class="elevation-1" sort-by="fullname" :items-per-page="30">
    <template v-slot:top>
      <v-toolbar flat color="white">
        <v-toolbar-title>
          Documents
        </v-toolbar-title>
        <v-spacer></v-spacer>
        <v-tooltip bottom >
          <template v-slot:activator="{ on }">
            <v-btn v-on="on" @click="addDoc()" fab outlined 
                  color="deep-purple">
              <v-icon>add</v-icon>
            </v-btn>
          </template>
          <span>Add Document</span>
         </v-tooltip>
      </v-toolbar>
      <v-row justify="space-around">
        Filters
        <v-col cols=2>
            <v-checkbox hide-details dense v-model="page" label="Pages" 
              @change="fetchDoc"/>
        </v-col>
        <v-col cols=2>
            <v-checkbox hide-details dense v-model="article" label="Articles" 
              @change="fetchDoc"/>
        </v-col>
        <v-col cols=2>
            <v-checkbox hide-details dense v-model="calendaritem" 
              label="Calendar Items" @change="fetchDoc"/>
        </v-col>
        <v-col cols=2>
            <v-checkbox hide-details dense v-model="active" label="Active" 
              @change="fetchDoc"/>
        </v-col>
      </v-row>
    </template>
    <template v-slot:item.action="{ item }">
      <v-icon small class="mr-2"  @click="editDoc(item)" >
        edit
      </v-icon>
    </template>
    <template v-slot:no-data>
      No documents yet.
    </template>            
  </v-data-table>
</v-container>

</template>

<script>

import api from '@/util/api'
import { mapState } from 'vuex'


export default {

  name: 'DocList',

  data () {return {
    headers: [
      {
        text: "Name", value: 'name'
      },
      {
        text: "Created", value: 'created'
      },
      {
        text: "Modified", value: 'modified'
      },
      {
        text: 'Actions', value: 'action', sortable: false
      }
    ],
    footerprops: {
      "items-per-page-options": [15,30,50,-1],
    },
    active: false,
    article: false,
    calendaritem: false,
    docs: [],
    page: false,
  }},

  computed: {
    ...mapState(['token'])
  },


  methods: {

    addDoc () {
      this.$router.push('/mgmt/doc/add')
    },
    
    editDoc (item) {
      this.$router.push('/mgmt/doc/edit/'  + item.id)
    },
    
    fetchDoc () {
      let dt = [], 
          params = { Authorization: 'Bearer ' + this.token };
      if (this.page) dt.push('page');
      if (this.article) dt.push('article');
      if (this.calendaritem) dt.push('calendar');
      if (dt.length) params.doctype = dt.join(',');
      if (this.active) params.active = "1";
      api('getDocs', params).then(
        function(data) {
          this.docs = data.documents;
          this.docs.forEach(function(p){
            p.created = (new Date(p.creationtime)).toLocaleString();
            p.modified = (new Date(p.modificationtime)).toLocaleString();
          }.bind(this));
        }.bind(this),
        function(data){
          if (data.status == 401) {
            this.$router.push('/mgmt/login')
          }
          else {
            console.error('getting getDocuments', data);
          }
        }.bind(this)
      );
    }

  },

  mounted () {
    this.fetchDoc()
  },  

}
</script>
