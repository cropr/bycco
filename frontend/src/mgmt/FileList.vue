<template>

<v-container>
  <h1>Management Files</h1>
  <v-data-table :headers="headers" :items="files"
      class="elevation-1" sort-by="fullname">
    <template v-slot:top>
      <v-toolbar flat color="white">
        <v-toolbar-title>
          Files
        </v-toolbar-title>
        <v-spacer></v-spacer>
        <v-tooltip bottom >
          <template v-slot:activator="{ on }">
            <v-btn v-on="on" @click="addFile()" fab outlined 
                  color="deep-purple">
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </template>
          <span>Add File</span>
         </v-tooltip>
      </v-toolbar>
    </template>
    <template v-slot:item.action="{ item }">
      <v-icon small class="mr-2"  @click="editFile(item)" >
        mdi-pencil
      </v-icon>
    </template>
    <template v-slot:item.topic_ts="{ item }">
      <date-formatted :date="item.topic_ts" fmt="ll" />
    </template>
    <template v-slot:no-data>
      No files yet.
    </template>            
  </v-data-table>
</v-container>

</template>

<script>

import { mapState } from 'vuex'
import { bearertoken } from "@/util/token"
import DateFormatted from "@/components/DateFormatted"
import * as moment from 'moment';

export default {

  name: 'FileList',

  data () {return {
    headers: [
      {
        text: "Name", value: 'name'
      },
      {
        text: "Topic", value: 'topic'
      },
      {
        text: "Topic timestamp", value: 'topic_ts'
      },
      {
        text: 'Actions', value: 'action', sortable: false
      }
    ],    
    files: [],
  }},

  computed: {
    ...mapState(['token', 'api'])
  },

  components: {
    DateFormatted,
  },

  methods: {

    addFile () {
      this.$router.push('/mgmt/file/add')
    },

    editFile (item) {
      this.$router.push('/mgmt/file/edit/'  + item.id)
    },
    
    getFiles() {
      let self=this;
      this.api.get_files(
        {},
        {securities: bearertoken(this.token)},
      ).then(
        function(data) {
          self.files = data.obj.files;
        },
        function(data){
          if (data.status == 401) {
            self.$router.push('/mgmt/login')
          }
          else {
            console.error('getting getFiles', data);
          self.$root.$emit('snackbar', {text: 'Getting files failed', reason: data})            
          }
        }
      );
    }
    
  },

  mounted () {
    moment.locale(this.locale)
    this.getFiles();
  },  

}
</script>
