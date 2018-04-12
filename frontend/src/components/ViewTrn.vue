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
      <h3 class="white--text">
        <span class="hidden-xs-only" v-text="_t['Tournament Results']"></span>
        <span v-text="cat"></span>
        <span class="hidden-xs-only" v-text="_t['Round']">
        </span> <span v-text="round"></span>
      </h3>
    </v-toolbar-title>
    <v-spacer></v-spacer>
    <div class="hidden-sm-and-down">
      <span class="white--text" v-text="_t.Category"></span>:
      <span class="white--text" v-text="cat"></span>
      <v-menu bottom left min-width="100px">
        <v-btn icon slot="activator" class="white--text">
          <v-icon>arrow_drop_down</v-icon>
        </v-btn>
        <v-list>
          <v-layout row>
            <v-list-tile sm6 @click="gotoCat('B8')">B8</v-list-tile>
            <v-list-tile sm6 @click="gotoCat('G8')">G8</v-list-tile>
          </v-layout>
          <v-layout row>
            <v-list-tile sm6 @click="gotoCat('B10')">B10</v-list-tile>
            <v-list-tile sm6 @click="gotoCat('G10')">G10</v-list-tile>
          </v-layout>
          <v-layout row>
            <v-list-tile sm6 @click="gotoCat('B12')">B12</v-list-tile>
            <v-list-tile sm6 @click="gotoCat('G12')">G12</v-list-tile>
          </v-layout>
          <v-layout row>
            <v-list-tile sm6 @click="gotoCat('B14')">B14</v-list-tile>
            <v-list-tile sm6 @click="gotoCat('G14')">G14</v-list-tile>
          </v-layout>
          <v-layout row>
            <v-list-tile sm6 @click="gotoCat('B16')">B16</v-list-tile>
            <v-list-tile sm6 @click="gotoCat('G16')">G16</v-list-tile>
          </v-layout>
          <v-layout row>
            <v-list-tile sm6 @click="gotoCat('B18')">B18</v-list-tile>
            <v-list-tile sm6 @click="gotoCat('G18')">G18</v-list-tile>
          </v-layout>
          <v-layout row>
            <v-list-tile sm6 @click="gotoCat('B20')">B20</v-list-tile>
            <v-list-tile sm6 @click="gotoCat('G20')">G20</v-list-tile>
          </v-layout>
       </v-list>
      </v-menu>
      <span class="white--text" v-text="_t.Round"></span>:
      <span class="white--text" v-text="round"></span>
      <v-menu bottom left min-width="100px">
        <v-btn icon slot="activator" class="white--text">
          <v-icon>arrow_drop_down</v-icon>
        </v-btn>
        <v-list>
          <v-layout row>
            <v-list-tile sm4 @click="gotoRound('1')">1</v-list-tile>
            <v-list-tile sm4 @click="gotoRound('2')">2</v-list-tile>
            <v-list-tile sm4 @click="gotoRound('3')">3</v-list-tile>
          </v-layout>
          <v-layout row>
            <v-list-tile sm4 @click="gotoRound('4')">4</v-list-tile>
            <v-list-tile sm4 @click="gotoRound('5')">5</v-list-tile>
            <v-list-tile sm4 @click="gotoRound('6')">6</v-list-tile>
          </v-layout>
          <v-layout row>
            <v-list-tile sm4 @click="gotoRound('7')">7</v-list-tile>
            <v-list-tile sm4 @click="gotoRound('8')">8</v-list-tile>
            <v-list-tile sm4 @click="gotoRound('9')">9</v-list-tile>
          </v-layout>
       </v-list>
      </v-menu>
    </div>
    <div class="hidden-md-and-up">
      <v-btn flat icon color="white" @click.stop="subdrawer = !subdrawer">
        <v-icon>more_vert</v-icon>
      </v-btn>
    </div>
  </v-toolbar>

  <v-tabs light slider-color="pink" v-model="tabix">
    <v-tab class="mx-2">
      <span v-text="_t.Pairings"></span>
    </v-tab>
    <v-tab class="mx-2">
      <span v-text="_t.Standings"></span>
    </v-tab>
    <v-tab class="mx-2">
      <span v-text="_t['Live Games']"></span>
    </v-tab>
    <v-tab class="mx-2">
      <span v-text="_t.Files"></span>
    </v-tab>
  </v-tabs>
  <v-tabs-items v-model="tabix">
    <v-tab-item>
      <view-trn-pairings :updateTrn="updateTrn"></view-trn-pairings>
    </v-tab-item>
    <v-tab-item>
      <view-trn-standings :updateTrn="updateTrn"></view-trn-standings>
    </v-tab-item>
    <v-tab-item>
      <view-trn-live :trn="trn"></view-trn-live>
    </v-tab-item>
    <v-tab-item>
      <view-trn-files :updateTrn="updateTrn"></view-trn-files>
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
      _t: {},
      catitems: ['B8', 'G8', 'B10', 'G10', 'B12', 'G12', 'B14', 'G14',
        'B16', 'G16', 'B18', 'G18', 'B20', 'G20'
      ]
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
          if ('id' in self.trn ) {
            self.trn = t;
            self.updateTrn = {
              trn: t,
              round: self.round
            };
          }
          else {
            api('getTopround', {
              id_trn: t.id,
            }).then(
              function(data){
                self.trn = t;
                self.round = data;
                self.updateTrn = {
                  trn: t,
                  round: self.round
                };
              },
              function(data) {
                console.error('failed getting topround', data);
              }
            );
          }
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
    openCat () {

    }
  },
  mounted () {
    var self=this;
    api('getTournaments').then(
      function(data) {
        self.trns = data.trns;
        self.gotoCat(self.cat);
      }
    );
    _.forEach(window._t, function(v,k){
      self._t[k] = v;
    })
  },
}
</script>

<style>
</style>
