<template>

<v-container>
  <h1>edit Page: {{page.maintitle}} </h1>

</v-container>

</template>

<script>

import api from '@/util/api'

export default {

  name: 'Pages',

  data () {return {
    headers: [
      {
        text: "Name", value: 'metatitle'
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

  mounted () {
    api('getPages', {}).then(
      function(data) {
        this.pages = data;
        this.pages.forEach(function(p){
          p.created = (new Date(p.creationtime)).toLocaleString();
          p.modified = (new Date(p.modificationtime)).toLocaleString();
        }.bind(this));
      }.bind(this),
      function(data){
        console.error('getting get pages', data);
      }
    );
  },  

}
</script>
