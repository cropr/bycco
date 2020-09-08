<template>
<v-container grid-list-md class="elevation-1">
  <v-row>
    <v-col cols=9>
      <h1>New Page</h1>
    </v-col>
    <v-col cols=3>
      <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn v-on="on" @click="back()" fab outlined 
                  color="deep-purple">
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </template>
          <span>Go Back</span>
      </v-tooltip>
      <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn v-on="on" @click="save()" fab outlined 
                  color="deep-purple">
              <v-icon>mdi-content-save</v-icon>
            </v-btn>
          </template>
          <span>Save changes</span>
      </v-tooltip>
    </v-col>
  </v-row>
  <v-row>
    <v-col cols=12 sm=6>
      <v-text-field label="Name" v-model="name" />
      <v-select :items="doctypes" label="Document type" v-model="doctype" />      
    </v-col>
  </v-row>
</v-container>
</template>

<script>

import { mapState } from 'vuex'
import { bearertoken } from "@/util/token"
import { doctypes } from '@/util/cms'

export default {
  
  name: "PageAdd",

  data () {return {
    name: '',
    doctype: null,
    doctypes: doctypes,
  }},

  computed: {
    ...mapState(['token', 'api'])
  },

  methods: {

    back () {
      this.$router.back();
    },

    save () {
      let self=this;
      this.api.create_page({}, {
        requestBody: {
          'name': this.name,
          'doctype': this.doctype,
        },
        securities: bearertoken(this.token),
      }).then(
        function(data){
          self.$root.$emit('snackbar', {text: 'Page created'})
          self.$router.push('/mgmt/page/edit/'  + data.body)
        },
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