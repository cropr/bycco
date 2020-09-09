<template>
<v-container>
  <h1>New Page</h1>
  <v-card>
    <v-card-title color="grey lighten-4">
      &nbsp;
      <v-spacer />
      <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn v-on="on" @click="back()" fab outlined 
                  color="deep-purple">
              <v-icon>mdi-arrow-left</v-icon>
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
    </v-card-title>
    <v-card-text>
      <v-text-field label="Name" v-model="name" />
      <v-select :items="doctypes" label="Document type" v-model="doctype" />      
    </v-card-text>
  </v-card>
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
    ...mapState(['token', 'api', 'locale'])
  },

  methods: {

    back () {
      this.$router.back();
    },

    save () {
      let self=this;
      this.api.add_page({}, {
        requestBody: {
          'name': this.name,
          'doctype': this.doctype,
          'locale': 'nl',
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