<template>
<v-container class="elevation-1">
  <v-row>
    <v-col cols=12 sm=6>
        <h1>Edit file: {{ name }} </h1>
    </v-col>
    <v-col col=12 sm=6>
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" outlined fab color="deep-purple" @click="back()" 
              slot="activator">
            <v-icon>mdi-arrow-left</v-icon>
          </v-btn>
        </template>
        <span>Go Back</span>
      </v-tooltip>
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" outlined fab color="deep-purple" @click="save()" 
              slot="activator">
            <v-icon>mdi-content-save</v-icon>
          </v-btn>
        </template>
        <span>Save file properties</span>
      </v-tooltip>
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" outlined fab color="deep-purple" @click="remove()" 
              slot="activator">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </template>
        <span>Delete file</span>
      </v-tooltip>
    </v-col>
  </v-row>
  <v-row>
    <v-col cols=12 sm=6>
      <v-text-field label="Name" v-model="f.name" />
      <v-text-field label="Owner" v-model="f.created_by" />
      <v-select :items="topictypes" label="Topic" v-model="f.topic" />         
    </v-col>
    <v-col cols=12 sm=6>
      <p>File created: <date-formatted :date="f.created_ts"/></p>
      <p>File modified: <date-formatted :date="f.modified_ts"/></p>
      <p>URL: <a :href="'/api/filecontent/' +  f.url">/api/filecontent/{{ f.url}}</a> </p>
      <v-menu v-model="menu_topic_ts" :close-on-content-click="false"
        :nudge-right="40" transition="scale-transition"
        offset-y min-width="290px"
      >
        <template v-slot:activator="{ on }">
          <v-text-field v-model="f.topic_ts" label="Topic date" prepend-icon="mdi-calendar-range"
            readonly v-on="on" />
        </template>
        <v-date-picker v-model="f.topic_ts" @input="menu_topic_ts = false" color="deep-purple" />
      </v-menu>
    </v-col>
  </v-row>
</v-container>
</template>

<script>

// import 'filepond/dist/filepond.min.css';
// import vueFilePond from 'vue-filepond';

import { mapState } from 'vuex'
import { bearertoken } from "@/util/token"
import DateFormatted from '@/components/DateFormatted.vue'
import { topictypes } from '@/util/cms'


// const FilePond = vueFilePond();

export default {

  name: "FileEdit",

  components: {
    DateFormatted,
  },

  computed: {
    ...mapState(['token', 'api']),
  },

  data () {return {
    f: {},
    menu_topic_ts: false,
    name: '', 
    topictypes: topictypes,   
    yesno: [
      {value:true, text: 'Yes'},
      {value:false, text: 'No'}
    ],
  }},

  methods: {

    back () {
      this.$router.push('/mgmt/file/list');
    },

    getFile() {
      let self=this;
      this.api.get_file(
        {id: this.$route.params.id},
        {securities: bearertoken(this.token)},
      ).then(
        function(data) {
          self.readFile(data.obj.file);
        },
        function(data){
          console.error('failed get file', data)
          self.$root.$emit('snackbar', {text: 'Getting file failed', reason: data})          
        }
      );
    },

    preview () { },

    publish() { },

    readFile (file) {
      this.f = file;
      this.name = this.f.name + '';
    },

    remove () {
      let self=this;
      if (window.confirm('Are you sure to delete file "' + this.name + '"?')) {
        this.api.delete_file(
          { id: this.$route.params.id },
          {securities: bearertoken(this.token)},
        ).then(
          function(){
            // TODO show deleted
            console.log('successfully deleted file')
            self.back();
          }, 
          function(data){
            // TODO show error message
            console.error('failed to delete', data);
          }
        );
      }
    },

    save () {
      let self=this;
      const {id, ...file} = this.f;
      console.log('saving', file);
      this.api.update_file({id},{
        requestBody: file,
        securities: bearertoken(this.token),        
      }).then(
        function(){
          // TODO successfully saved
          console.log('successfully saved file')
          self.$root.$emit('snackbar', {text: 'File saved'})          
        },
        function(data){
          // TODO show error message
          console.error('failed to save', data);
          self.$root.$emit('snackbar', {text: 'Saving file failed', reason: data})          
          self.back();
        }
      );
    },

    toggleLang(l){
      this.p.languages = this.enabledLang;
      if (l in this.p.file_i18n_fields === false) {
        this.p.file_i18n_fields[l] = {
          body: '',
          intro: '',
          title: '',
        }
      }
    },
  },

  mounted () {
    this.getFile();
  }

}
</script>

<style scoped>
.bordermd {
  border: 1px solid grey;
}
</style>