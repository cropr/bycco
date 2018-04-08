<template>
<div>
  <v-navigation-drawer temporary fixed clipped v-model="subdrawer" right
                      class="navmax blue-grey lighten-2">
    <v-toolbar flat class="blue-grey">
      <v-toolbar-title class="white--text">Series</v-toolbar-title>
    </v-toolbar>
    <v-layout>
      <v-flex>
        <v-btn @click="gotoCat('B8')" flat icon>B8</v-btn>
      </v-flex>
      <v-flex>
        <v-btn @click="gotoCat('G8')" flat icon>G8</v-btn>
      </v-flex>
    </v-layout>
    <v-layout>
      <v-flex>
        <v-btn @click="gotoCat('B10')" href="#" flat icon>B10</v-btn>
      </v-flex>
      <v-flex>
        <v-btn @click="gotoCat('G10')" flat icon>G10</v-btn>
      </v-flex>
    </v-layout>
    <v-layout>
      <v-flex>
        <v-btn @click="gotoCat('B12')" flat icon>B12</v-btn>
      </v-flex>
      <v-flex>
        <v-btn @click="gotoCat('G12')" flat icon>G12</v-btn>
      </v-flex>
    </v-layout>
    <v-layout>
      <v-flex>
        <v-btn @click="gotoCat('B14')" flat icon>B14</v-btn>
      </v-flex>
      <v-flex>
        <v-btn @click="gotoCat('G14')" flat icon>G14</v-btn>
      </v-flex>
    </v-layout>
    <v-layout>
      <v-flex>
        <v-btn @click="gotoCat('B16')" flat icon>B16</v-btn>
      </v-flex>
      <v-flex>
        <v-btn @click="gotoCat('G16')" flat icon>G16</v-btn>
      </v-flex>
    </v-layout>
    <v-layout>
      <v-flex>
        <v-btn @click="gotoCat('B18')" flat icon>B18</v-btn>
      </v-flex>
      <v-flex>
        <v-btn @click="gotoCat('G18')" flat icon>G18</v-btn>
      </v-flex>
    </v-layout>
    <v-layout>
      <v-flex>
        <v-btn @click="gotoCat('B20')" flat icon>B20</v-btn>
      </v-flex>
      <v-flex>
        <v-btn @click="gotoCat('G20')" flat icon>G20</v-btn>
      </v-flex>
    </v-layout>
    <v-toolbar flat class="blue-grey">
      <v-toolbar-title class="white--text">Round</v-toolbar-title>
    </v-toolbar>
    <v-layout row>
      <v-flex>
        <v-btn @click="gotoRound('1')" flat icon>1</v-btn>
      </v-flex>
      <v-flex>
        <v-btn @click="gotoRound('2')" flat icon>2</v-btn>
      </v-flex>
      <v-flex>
        <v-btn @click="gotoRound('3')" flat icon>3</v-btn>
      </v-flex>
    </v-layout>
    <v-layout>
      <v-flex>
        <v-btn @click="gotoRound('4')" flat icon>4</v-btn>
      </v-flex>
      <v-flex>
        <v-btn @click="gotoRound('5')" flat icon>5</v-btn>
      </v-flex>
      <v-flex>
        <v-btn @click="gotoRound('6')" flat icon>6</v-btn>
      </v-flex>
    </v-layout>
    <v-layout>
      <v-flex>
        <v-btn @click="gotoRound('7')" flat icon>7</v-btn>
      </v-flex>
      <v-flex>
        <v-btn @click="gotoRound('8')" flat icon>8</v-btn>
      </v-flex>
      <v-flex>
        <v-btn @click="gotoRound('9')" flat icon>9</v-btn>
      </v-flex>
    </v-layout>
  </v-navigation-drawer>
  <v-toolbar color="blue-grey lighten-2">
    <v-toolbar-title>
      <h3 class="white--text">Tournament Results <span v-text="cat"></span>
        Round <span v-text="round"></span>
      </h3>
    </v-toolbar-title>
    <v-spacer></v-spacer>
    <v-btn flat icon color="white" @click.stop="subdrawer = !subdrawer">
      <v-icon>more_vert</v-icon>
    </v-btn>
  </v-toolbar>

  <v-tabs light slider-color="pink" v-model="tabix">
    <v-tab class="mx-2">
      Pairings
    </v-tab>
    <v-tab class="mx-2">
      Standings
    </v-tab>
    <v-tab class="mx-2">
      Live Games
    </v-tab>
    <v-tab class="mx-2">
      Files
    </v-tab>
  </v-tabs>
  <v-tabs-items v-model="tabix">
    <v-tab-item>
      <view-trn-pairings :updateTrn="updateTrn"></view-trn-pairings>
    </v-tab-item>
    <v-tab-item>
      <view-trn-standings :trn="trn"></view-trn-standings>
    </v-tab-item>
    <v-tab-item>
      <view-trn-live :trn="trn"></view-trn-live>
    </v-tab-item>
    <v-tab-item>
      <view-trn-files :trn="trn"></view-trn-files>
    </v-tab-item>
  </v-tabs-items>

</div>
</template>

<script>
import api from '../api/api';
import _ from 'lodash';
import ViewTrnPairings from './ViewTrnPairings';
import ViewTrnStandings from './ViewTrnStandings';
import ViewTrnLive from './ViewTrnLive';
import ViewTrnFiles from './ViewTrnFiles';

const catmapping = {
  G8: 'BG8',
  B8: 'BG8',
  G10: 'G10',
  B10: 'B10',
  G12: 'G12',
  B12: 'B12',
  G14: 'G14',
  B14: 'B14',
  G16: 'G16',
  B16: 'B16',
  G18: 'BG18',
  B18: 'BG18',
  G20: 'BG20',
  B20: 'BG20',
};

export default {
  components: {
    "view-trn-pairings": ViewTrnPairings,
    "view-trn-standings": ViewTrnStandings,
    "view-trn-live": ViewTrnLive,
    "view-trn-files": ViewTrnFiles,
  },
  data () {
    return {
      trn: {},
      updateTrn: {},
      trns: [],
      cat: 'B8',
      round: "1",
      subdrawer: false,
      tabix: '0',
      pairings:[],
    }
  },
  methods: {
    gotoCat (cat) {
      console.log('Going to cat ', cat, this.trns);
      var self=this;
      this.cat = catmapping[cat];
      this.subdrawer = false;
      _.forEach(this.trns, function(t){
        if (t.shortname == self.cat) {
          self.trn = t;
          self.updateTrn = {
            trn: t,
            round: self.round
          };
        }
      })
    },
    gotoRound (r) {
      console.log('Going to round ', r);
      this.round = r;
      this.subdrawer = false;
      this.updateTrn = {
        trn: this.trn,
        round: r
      };
    },
  },
  mounted () {
    var self=this;
    api('getTournaments').then(
      function(data) {
        self.trns = data.trns;
        self.gotoCat(self.cat);
      }
    )
  },
}
</script>

<style>
</style>
