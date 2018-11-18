<template>
<div>
  <h2>{{$t('Photo')}}</h2>
  <h4 class="mt-2">{{$t('Select photo')}}</h4>
  <div>{{$t('SubPhoto1')}}</div>
  <div class="my-1">
    <file-pond ref="pond" accepted-file-types="image/jpeg, image/png"
        @addfile="handleFile" :labelIdle="labelIdle" className="dropbox" />
  </div>
  <div class="photosrc">
    <vue-cropper ref='photosrc' :view-mode="2" drag-mode="crop" :auto-crop-area="0.5"
                 :background="true" src="" alt="Source Image" :aspect-ratio="0.8"
                 preview="#photoresult" :img-style="{height: '400px'}">
    </vue-cropper>
  </div>
  <h4 class="mt-2">{{$t('Resulting photo')}}</h4>
  <div>{{$t('SubPhoto3')}}</div>
  <div id="photoresult" class="photoresult"></div>
  <div class="mt-2">
    <v-btn @click="doCrop" color="primary">{{$t('Continue')}}
    </v-btn>
    <v-btn @click="prev">{{$t('Back')}}
    </v-btn>
  </div>

</div>
</template>

<script>
import VueCropper from 'vue-cropperjs';
import vueFilePond from 'vue-filepond';
import 'filepond/dist/filepond.min.css';

import api from '../util/api'
import { mapState } from 'vuex'

const FilePond = vueFilePond();

export default {

  name: "SubscriptionPhoto",

  computed: {
    labelIdle () {
      return '<span class="filepond--label-action">' + this.$t('SubPhoto2') + '</span>';
    },
    ...mapState(['subscription', 'flow', 'photo']),
  },

  components: {
    VueCropper,
    FilePond,
  },

  watch: {
    photo (nv) {
      if (!nv.length) {
        console.log('trying to empty photo');
        this.$refs.pond.removeFiles();
        this.$refs.photosrc.destroy();
      }
    }
  },

  methods: {

    doCrop() {
      this.$store.commit('setPhoto', this.$refs.photosrc.getCroppedCanvas({width: 160}).toDataURL());
      if (!this.photo.length) {
          this.$store.commit('updateFlow',{step: this.flow.step + 1})
          return
      }
      api('uploadPhoto', {
        photo: this.photo,
        idsub: this.subscription.idsub,
      }).then(
        function(){
            this.$store.commit('updateFlow',{step: this.flow.step + 1})
        }.bind(this),
        function(err){
          console.log('upload failed', err)
        }
      );
    },

    handleFile(err, file){
      const reader = new FileReader();
      reader.onload = (event) => {
        this.$refs.photosrc.replace(event.target.result);
      };
      reader.readAsDataURL(file.file);
    },

    prev () {
      this.$store.commit('updateFlow', {step: this.flow.step-1})
    },

  }

}
</script>

<style>
.dropbox {
  width: 100%;
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