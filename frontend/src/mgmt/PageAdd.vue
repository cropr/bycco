<template>
<v-container fluid grid-list-md class="elevation-1">
  <v-layout row wrap>
    <v-flex>
        <h1>New Article</h1>
    </v-flex>
    <v-flex>
      <v-tooltip bottom>
        <v-btn outline fab color="green" @click="back()" slot="activator">
          <v-icon>arrow_back</v-icon>
        </v-btn>
        <span>Go Back</span>
      </v-tooltip>
      <v-tooltip bottom>
        <v-btn outline fab color="green" @click="save()" slot="activator">
          <v-icon>save</v-icon>
        </v-btn>
        <span>Save changes</span>
      </v-tooltip>
    </v-flex>
  </v-layout>
  <v-layout row wrap>
    <v-flex sm6 xs12>
      <v-text-field label="Author" v-model="p.author" />
      <v-text-field label="title" v-model="p.maintitle" />
    </v-flex>

  </v-layout>

</v-container>
</template>

<script>

import api from '../util/api'

export default {
  
  name: "PageAdd",

  data () {return {
    p: { mainlocale: window.config.lang},
  }},

  methods: {

    back () {
      this.$emit('update', {section: 'list', params:{}})
    },

    save () {
      
      api('addArticle', {
        article: this.p,
      }).then(
        function(data){
          console.log('id received', data)
          this.$emit('update', {
            section: 'edit', 
            article: {id: data.id}, 
            reload: true,
            text: 'Article created.'
          })
        }.bind(this),
        function(data){
          console.error('failed to save', data);
        }
      );
    },
  },


}
</script>

<style scoped>

.dropbox {
  width: 100%;
  height: 100px;
}

</style>