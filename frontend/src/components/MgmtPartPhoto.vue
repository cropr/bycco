<template>
<v-container fluid grid-list-md class="elevation-1">
 
  <v-layout row wrap>
    <v-flex>
      <h1>Photo Participant: {{ fullname }} </h1>
    </v-flex>
    <v-flex>
      <v-tooltip bottom>
        <v-btn outline fab color="blue-grey" @click="back()" slot="activator">
          <v-icon>arrow_back</v-icon>
        </v-btn>
        <span>Go Back</span>
      </v-tooltip>
      <v-tooltip bottom>
        <v-btn outline fab color="blue-grey" @click="crop()" slot="activator">
          <v-icon>crop</v-icon>
        </v-btn>
        <span>Crop image</span>
      </v-tooltip>      
      <v-tooltip bottom>
        <v-btn outline fab color="blue-grey" @click="save()" slot="activator">
          <v-icon>save</v-icon>
        </v-btn>
        <span>Save</span>
      </v-tooltip>
      <v-tooltip bottom>
        <v-btn outline fab color="blue-grey" @click="gotoEdit()" slot="activator">
          <v-icon>edit</v-icon>
        </v-btn>
        <span>Save</span>
      </v-tooltip>            
    </v-flex>
  </v-layout>
 
  <v-layout row wrap>
    <v-flex class="my-1">
      <h4>Existing Photo</h4>
      <div><img :src="photosrc"></div>
    </v-flex>
    <v-flex class="my-1">
      <h4>Resulting Photo</h4>
      <div><img :src="photo"></div>
    </v-flex>
  </v-layout>

  <div class="mt-2">
    <h4>Drop Area</h4>
    <file-pond ref="pond" accepted-file-types="image/jpeg, image/png"
        @addfile="handleFile" className="dropbox" /> 
  </div>
  
  <div  class="mt-2">
    <h4>Photo Selection</h4>
    <div class="photosrc">
      <vue-cropper ref='photosrc' :view-mode="2" drag-mode="crop" :auto-crop-area="0.5"
                  :background="true" src="" alt="Source Image" :aspect-ratio="0.8"
                  preview="#photoresult" :img-style="{height: '400px'}">
      </vue-cropper>
    </div>        
  </div>

</v-container>
</template>

<script>

import api from '../util/api'
import 'filepond/dist/filepond.min.css';
import DateFormatted from "./DateFormatted";
import VueCropper from 'vue-cropperjs';
import vueFilePond from 'vue-filepond';

const FilePond = vueFilePond();

export default {
  name: "MgmtPartEdit",

  components: {
    DateFormatted,
    VueCropper,
    FilePond,
  },

  props: ['participant'],

  computed :  {
    fullname () {
      return this.participant.first_name + ' ' + this.participant.last_name;
    },
  },

  data () {return {
    p: {},
    photosrc: '',
    photo: '',
  }},

  methods: {

    back () {
      this.$emit('update', {section: 'list', params:{}})
    },

    crop() {
      this.photo = this.$refs.photosrc.getCroppedCanvas({width: 160}).toDataURL();
    },

    getAttendee () {
      api('getAttendee', {
        id: this.participant.id
      }).then(
      function(data) {
          this.p = data.attendee;
          this.photosrc =  this.p.id ? '/api/subscriptions/' + this.p.id + 
            '/photo?time=' + (new Date()).getTime() : 
        '/static/img/nobody.png';
          this.photo = '';
        }.bind(this)
      )
    },

    gotoEdit () {
      this.$emit('update', {section: 'edit', params: this.participant})
    },    

    handleFile(err, file){
      const reader = new FileReader();
      reader.onload = (event) => {
        this.$refs.photosrc.replace(event.target.result);
      };
      reader.readAsDataURL(file.file);
    },
    
    save() {
      api('uploadPhoto', {
        photo: this.photo,
        idsub: this.p.id,
      }).then(
        function(){
          this.$emit('update', {
            section: 'photo', 
            text: 'Photo saved',
            reload: true,
            params: this.participant,
          });
          this.getAttendee()
        }.bind(this),
        function(err){
          console.log('upload failed', err)
        }
      );
    }

  },

  mounted () {
    this.getAttendee()
  }

}
</script>

<style>
.dropbox {
  width: 100%;
  height: 100px;
}
.photosrc{
  overflow: hidden;
  width: 100%;
  height: 400px;
  border: 1px dashed #808080;
  background-color: #d3d3d3;
}
.photoresult {
  overflow: hidden;
  position: relative;
  text-align: center;
  width: 160px;
  height: 200px;
}
</style>