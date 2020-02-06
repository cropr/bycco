<template>
<v-container fluid grid-list-md class="elevation-1">
  <v-row>
    <v-col cols=9>
      <h1>New Article</h1>
    </v-col>
    <v-col cols=3>
      <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn v-on="on" @click="back()" fab outlined 
                  color="deep-purple">
              <v-icon>add</v-icon>
            </v-btn>
          </template>
          <span>Go Back</span>
      </v-tooltip>
      <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn v-on="on" @click="save()" fab outlined 
                  color="deep-purple">
              <v-icon>save</v-icon>
            </v-btn>
          </template>
          <span>Save changes</span>
      </v-tooltip>
    </v-col>
  </v-row>
  <v-row>
    <v-col cols=12 sm=6>
      <v-text-field label="Author" v-model="author" />
      <v-text-field label="Name" v-model="name" />
      <v-select :items="dt" v-model="doctype" label="Document type" />
    </v-col>
  </v-row>
</v-container>
</template>

<script>

import api from '@/util/api'
import {doctypes} from '@/util/const'

export default {
  
  name: "DocAdd",

  data () {return {
    name: '',
    author: '',
    doctype: 'article',
    dt: [],
  }},

  methods: {

    back () {
    },

    save () {
      
      api('addDoc', {
        document: {
          'name': this.name,
          'owner': this.author,
          'doctype': this.doctype,
        }
      }).then(
        function(data){
          console.log('page created', data)
          this.$router.push('/mgmt/doc/edit/'  + data.id)
        }.bind(this),
        function(data){
          console.error('failed to save', data);
        }
      );
    },
  },

  mounted () {
    doctypes.forEach(function(v){
      this.dt.push({value: v[0], text:v[1]})
    }.bind(this))
  }

}
</script>

<style scoped>

.dropbox {
  width: 100%;
  height: 100px;
}

</style>