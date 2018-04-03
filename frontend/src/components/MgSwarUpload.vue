<template>
<div >

  <v-layout>
    <v-flex xs12 sm6>
      <v-card class="mt-2 mb-2 ml-2 mr-2" light>
        <v-card-title class="blue-grey lighten-4 headline">
          Upload JSON file of SWAR
        </v-card-title>
        <v-card-text>
          <p>
            Drag the json file in the upload area below of click in the
            upload area and select the file
          </p>
          <drop class="drop" @drop="dropped">
            Drop SWAR json file here
          </drop>
        </v-card-text>
      </v-card>

    </v-flex>
  </v-layout>

  <v-layout>
    <v-flex xs12 sm6>
      <v-card class="mt-2 mb-2 ml-2 mr-2">
        <v-card-title class="blue-grey lighten-4 headline">
          Upload properties
        </v-card-title>
        <v-card-text>
          <div>Name of the tournament in swar:<b v-text="swarupload.name"></b>
          </div>
          <div>
            Current round of tournament in swar:<b v-text="swarupload.round"></b>
          </div>
          <div v-show="!swarupload.trn">
            We have not found a corresponding tournament in our database
          </div>
          <div v-show="swarupload.trn">
            We have found a corresponding tournament in our database
          </div>
          <v-radio-group v-model="ctrlswar.trnchoice">
            <v-radio value="linked" :disabled="!ctrlswar.trn">
              Use the corresponding tournament:
              <b v-text="swarupload.name" v-show="ctrlswar.trn"></b>
            </v-radio>
            <v-radio value="select" :disabled="!trns.length">
              Link an existing tournament to this SWAR file
            </v-radio>
          </v-radio-group>
          <v-select  v-show="ctrlswar.trnchoice == 'select'"
            label="Tournament" v-model="ctrlswar.linkedtrn" :items="trns">

          </v-select>
        </v-card-text>
        <v-card-actions>
          <v-btn class="blue-grey" color="primary" @click="upload()">
            Upload
          </v-btn>
        </v-card-actions>

      </v-card>
    </v-flex>
  </v-layout>

  <v-layout v-show="swartournaments.length">
    <v-flex xs12 sm6>
      <v-card class="mt-2 mb-2 ml-2 mr-2" light>
        <v-card-title class="blue-grey lighten-4 headline">
          Existing tournaments with uploaded swar files
        </v-card-title>
        <v-card-text>
          <v-layout v-for="(trn,ix) in swartournaments">
            <v-flex xs1 v-text="ix+1"></v-flex>
            <v-flex xs11 @click="opentrn(trn)">
              <b v-text="trn.shortname"></b>&nbsp;
              <span v-text="trn.swarname"></span>
            </v-flex>
          </v-layout>
        </v-card-text>
      </v-card>

    </v-flex>
  </v-layout>


</div>
</template>

<script>
import api from '../api/api';
import { Drag, Drop } from 'vue-drag-drop';


export default {
  props: ['trns'],
  data () {
    return {
      name: '',
      shortname: '',
      rounds: 9
    }
  },
  methods: {
    dropped (data, event) {
      event.preventDefault();
      const files = event.dataTransfer.files;
      const filenames = [];
      for (let i = 0; i < files.length; i++) {
        filenames.push(files.item(i).name);
      }
      alert(`You dropped files: ${JSON.stringify(filenames)}`);
    },
    gettrns () {
      var self = this;
      api('addTournament', {
        name: this.name,
        shortname: this.shortname,
        rounds: this.rounds
      }).then(
        function(data){
          ;
        },
        function(data) {
          console.error('adding trn failed', data)
        }
      )

    },
    opentrn (t) {
      console.log('opening trn', t);
      this.$emit('openTrn', t);
    }
  }
}
</script>

<style>
</style>
