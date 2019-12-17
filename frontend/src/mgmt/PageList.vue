<template>

<v-container>
  <h1>Management Pages</h1>
  <v-data-table :headers="headers" :items="pages"
      class="elevation-1" sort-by="fullname">
    <template v-slot:top>
      <v-toolbar flat color="white">
        <v-toolbar-title>
          Pages
        </v-toolbar-title>
        <v-spacer></v-spacer>
        <v-tooltip bottom >
          <template v-slot:activator="{ on }">
            <v-btn v-on="on" @click="addPage()" fab outlined 
                  color="deep-purple">
              <v-icon>add</v-icon>
            </v-btn>
          </template>
          <span>Add Page</span>
         </v-tooltip>
      </v-toolbar>
    </template>
    <template v-slot:item.action="{ item }">
      <v-icon small class="mr-2"  @click="editPage(item)" >
        edit
      </v-icon>
    </template>
    <template v-slot:no-data>
      No pages yet.
    </template>            
  </v-data-table>
</v-container>

</template>

<script>

import api from '@/util/api'
import { mapState } from 'vuex'


export default {

  name: 'PageList',

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
    pages: [],
  }},

  computed: {
    ...mapState(['token'])
  },


  methods: {
    editPage (item) {
      this.$router.push('/mgmt/page/edit/'  + item.id)
    }
  },

  mounted () {
    api('getPages', {
      Authorization: 'Bearer ' + this.token
    }).then(
      function(data) {
        this.pages = data.pages;
        this.pages.forEach(function(p){
          p.created = (new Date(p.creationtime)).toLocaleString();
          p.modified = (new Date(p.modificationtime)).toLocaleString();
        }.bind(this));
      }.bind(this),
      function(data){
        if (data.status == 401) {
          this.$router.push('/mgmt/login')
        }
        else {
          console.error('getting getPages', data);
        }
      }.bind(this)
    );
  },  

}
</script>
