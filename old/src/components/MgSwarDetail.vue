<template>
<div>
  <h4 class="ma-3">
    List of uploaded swar json files for:
    <span v-text="swartrn.swarname"></span>
  </h4>
  <v-card class="ma-2" light v-for="(sf, ix) in swarfiles" :key="sf.id"
          :class="{isActive: sf.status == 'ACT'}">
    <v-layout row>
      <v-flex xs1 class="vertical-align pa-2" v-text="ix+1"></v-flex>
      <v-flex xs1 class="vertical-align pa-2">Round: <b v-text="sf.round"></b></v-flex>
      <v-flex xs2 class="vertical-align pa-2">Upload date: <b v-text="sf.upldate"></b></v-flex>
      <v-flex xs2 class="vertical-align pa-2">status: <b v-text="sf.pub"></b></v-flex>
      <v-flex xs6 class="pa-2">
        <v-btn v-show="!sf.opened" @click="open(sf)">Open</v-btn>
        <v-btn v-show="sf.opened" @click="close(sf)">Close</v-btn>
        <v-btn v-show="canPublish(sf)" @click="publish(sf)">Publish</v-btn>
        <v-btn v-show="canDelete(sf)" @click="remove(sf)">Delete</v-btn>
      </v-flex>
    </v-layout>
    <div v-show="sf.opened">
      <mg-swar-file :swarfile="swarfileopened"></mg-swar-file>
    </div>
  </v-card>
</div>
</template>

<script>
import _ from 'lodash';
import api from '../api/api';
import moment from 'moment';
import MgSwarFile from './MgSwarFile';

const pubvalues = {
  UNP: 'Not published',
  ACT: 'Active',
  OUT: 'Outdated',
};

export default {
  props: ['swartrn', 'tabix'],
  data () {
    return {
      swarfiles: [],
      swarfileopened: {},
      pairings: [],
      bye: {},
      absences: [],
      players: [],
      p: {},
    }
  },
  components: {
    MgSwarFile,
    "mg-swar-file": MgSwarFile,
  },
  methods: {
    canDelete (sf ) {
      return sf.status != 'ACT';
    },
    canPublish (sf ) {
      return sf.status != 'ACT';
    },
    close (sf) {
      console.log('closing round', sf.round);
      sf.opened = false;
    },
    formatDate (d) {
      if (d) {
        return moment(d).format('DD/MM/YY HH:mm')
      }
      return '***';
    },
    getFiles () {
      var self=this;
      api('getSwarFiles', {id_swartrn: this.swartrn.id}).then(
        function(data) {
          self.swarfiles = [];
          _.forEach(data, function(v){
            v.upldate = self.formatDate(new Date(v.uploaddate));
            v.pub = pubvalues[v.status];
            v.opened = false;
            self.swarfiles.push(v);
          })
        },
        function(data){
          console.error('failed getting swar files', data);
        }
      )
    },
    open (sf) {
      var self=this;
      api('getSwarFile', {
        id_swartrn: this.swartrn.id,
        id_swarfile: sf.id
      }).then(
        function(data){
          sf.opened = true;
          self.swarfileopened = data;
        },
        function(data){
          console.error('Error getting swar file', data);
        }
      )
    },
    publish (sf) {
      var self=this;
      api('publishSwarFile', {
        id_swartrn: this.swartrn.id,
        id_swarfile: sf.id
      }).then(
        function(data) {
          console.log('published');
          self.getFiles();
        },
        function(data) {
          console.error('failed to publish round ', sf.round)
        }
      )
    },
    remove (sf) {
      var self=this;
      api('removeSwarFile', {
        id_swartrn: this.swartrn.id,
        id_swarfile: sf.id
      }).then(
        function(data) {
          console.log('removed');
          self.getFiles();
        },
        function(data) {
          console.error('failed to remove round ', sf.round)
        }
      )
    },
  },
  watch: {
    tabix: function(newVal, oldVal) {
      console.log('watch update', newVal);
      if (newVal == "1") {
        this.getFiles();
      }
    }
  }
}
</script>

<style scoped>
.vertical-align {
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.theme--light.card.isActive {
  background-color: #ebfbeb;
}
</style>
