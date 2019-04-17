<template>
<div >

  <v-layout>
    <v-flex xs12 sm6>
      <v-card class="ma-2" light>
        <v-card-title class="blue-grey lighten-4 headline">
          Upload JSON file of SWAR
        </v-card-title>
        <v-card-text>
          <p>
            Drag the json file in the upload area below
          </p>
          <drop class="drop" @drop="dropped" :class="{dragover: dragging}"
                @dragover="dragging = true" @dragleave="dragging = false">
            Drop SWAR json file here
          </drop>
        </v-card-text>
      </v-card>

    </v-flex>
  </v-layout>

  <v-layout v-show="swarname">
    <v-flex xs12 sm6>
      <v-card class="ma-2">
        <v-card-title class="blue-grey lighten-4 headline">
          Upload properties
        </v-card-title>
        <v-card-text>
          <div class="my-1">Name of the tournament in swar: <b v-text="swarname"></b>
          </div>
          <div class="my-1">
            Current round of tournament in swar: <b v-text="swarround"></b>
          </div>
          <div v-show="!swartrn" class="my-1">
            We have not found a corresponding tournament in our database.
            Select the tournamanet that is linked to this Swar file
          </div>
          <div v-show="swartrn"  class="my-1">
            We have found a corresponding tournament in our database
            <v-radio-group v-model="trnchoice" v-show="swartrn">
              <v-radio value="linked" :label="'Use the corresponding tournament: ' + swarname">
              </v-radio>
              <v-radio value="select" :label="'Link an existing tournament to this SWAR file'">
              </v-radio>
            </v-radio-group>
          </div>
          <v-select v-model="swartrnid" v-show="trnchoice == 'select'"
                    :items="trnsa" item-text="name" item-value="id"
                    label="Tournament" no-data-text="Select tournament">
          </v-select>
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="upload()">
            Upload
          </v-btn>
        </v-card-actions>

      </v-card>
    </v-flex>
  </v-layout>

  <v-layout v-show="swartrns.length">
    <v-flex xs12 sm6>
      <v-card class="ma-2" light>
        <v-card-title class="blue-grey lighten-4 headline">
          Existing tournaments with uploaded swar files
        </v-card-title>
        <v-card-text>
          <v-layout v-for="(st,ix) in swartrns" :key="st.id">
            <v-flex xs1 v-text="ix+1"></v-flex>
            <v-flex xs1 ><b v-text="st.shortname"></b></v-flex>
            <v-flex xs10>
              <a href="#" v-text="st.swarname" @click="openswar(st)"></a>
            </v-flex>
          </v-layout>
        </v-card-text>
      </v-card>

    </v-flex>
  </v-layout>


</div>
</template>

<script>
import api from '../util/api';
import { Drag, Drop } from 'vue-drag-drop';


export default {

  name: 'MgmtSwaOverview',

  props: ['swartrns'],

  components: {
    drop: Drop,
    drag: Drag,
  },
  
  data () {
    return {
      jsonfile: '',
      swarname: '',
      swarround: 1,
      swartrn: null,
      swartrnid: null,
      trnchoice: '',
      trns: {},
      trnsa: [],
      dragging: false,
    }
  },
  
  methods: {
    
    checktrns () {
      this.swartrns.forEach(function(v){
        console.log('name', v.swarname, v.id, v.tournament_id);
        if (v.swarname == this.swarname) {
          this.swartrn = v;
          this.trnchoice = 'linked';
          this.swartrnid = v.id;
        }
      })
    },

    dropped (data, event) {
      var reader = new FileReader(),
          file = event.dataTransfer.files[0],
          jsonswar;
      console.log('upload file', file)
      this.dragging = false;
      event.preventDefault();
      reader.onload = function (evt) {
        this.jsonfile = evt.target.result;
        jsonswar = JSON.parse(this.jsonfile).Swar;
        console.log('jsonswar', jsonswar);
        this.swarname = jsonswar.TournamentDesc.Tournament;
        this.swarround = jsonswar.Player[0].RoundArray ?
          jsonswar.Player[0].RoundArray.length : 0;
        this.trnchoice = 'select';
        this.checktrns();
      }.bind(this);
      if (file) {
        reader.readAsText(file);
      }
      else {
        console.log('No event file', event)
      }
    },
    
    getTournaments () {
      api('getTournaments').then(
        function (data) {
          this.trnsa = data.trns;
          this.trns =  {};
          data.trns.forEach(function(v){
            this.trns[v.id] = v;
          }.bind(this));
          console.log('trns loaded', this.trns)
        }.bind(this),
        function (data) {
          console.error('getting trns failed', data)
        }
      )
    },

    openswar (st) {
      this.$emit('openSwar', st);
    },

    upload () {
      api('uploadSwarJson', {
        name: this.swarname,
        round: this.swarround,
        id_trn: this.swartrnid,
        jsonfile: this.jsonfile,
      }).then(
        function(data){
          console.log('added swar succeeded', data);
          this.getTournaments();
        }.bind(this),
        function(data){
          console.error('adding swar failed', data);
        }
      )
    },

  },

  mounted () {
    this.getTournaments();
  }

}
</script>

<style scoped>
.drop {
  background: #F8F8F8;
  border: 5px dashed #DDD;
  width: 80%;
  height: 80px;
  text-align: center;
  padding-top: 15px;
  margin: 10px auto 10px auto;
}

.drop.dragover {
  border-color: #0000cc;
}

</style>
