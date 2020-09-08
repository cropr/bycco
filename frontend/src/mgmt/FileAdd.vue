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
    </v-col>
  </v-row>
  <h4>Drop Area</h4>
  <file-pond ref="pond" @addfile="handleFile" className="dropbox" /> 
</v-container>
</template>

<script>

import 'filepond/dist/filepond.min.css';
import vueFilePond from 'vue-filepond';

import { mapState } from 'vuex'
import { bearertoken } from "@/util/token"

const FilePond = vueFilePond();

export default {
  
  name: "FileAdd",

  components: {
    FilePond,
  },



  data () {return {
    content: '',
    f: {},
    name: '',
  }},

  computed: {
    ...mapState(['token', 'api'])
  },

  methods: {

    back () {
      this.$router.back();
    },

    handleFile(err, file){
      let self=this;
      const reader = new FileReader();
      console.log('file dropped', file);
      this.name = file.filename;
      reader.onload = function(event) {
        console.log('onload event ', event)
        self.content = reader.result.split(',')[1];
        console.log('content', self.content)
      };
      reader.readAsDataURL(file.file);
    },

    save () {
      let self=this;
      console.log('saving with token', this.token)
      this.api.create_file({}, {
        requestBody: {
          'name': this.name,
          'content': this.content,
        },
        securities: bearertoken(this.token),
      }).then(
        function(data){
          console.log('file created', data)
          self.$router.push('/mgmt/file/edit/'  + data.body)
          self.$root.$emit('snackbar', {text: 'File created'})          
        },
        function(data){
          console.error('failed to save', data);
          self.$root.$emit('snackbar', {text: 'File not created', reason: data})          
        }
      );
    },
  },


}
</script>

<style>

.dropbox {
  width: 100%;
  height: 100px;
}

</style>