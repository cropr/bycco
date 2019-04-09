<template>
  <v-app>
    <sidebar />
    <topbar />
    <v-toolbar fixed dark dense app class="blue-grey darken-1 subtoolbar">
      <v-toolbar-title>
        <h4 class="white--text">
          <span class="hidden-xs-only">
            {{$t('Tournament Results')}}
          </span>
          <span>{{cat}}</span>
          <span class="hidden-xs-only"> {{$t('Round')}}</span> 
          <span class="hidden-sm-and-up"> R</span> 
          <span>{{round}}</span>
        </h4>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <div class="hidden-md-and-up">
        <v-menu bottom left>
          <v-btn icon slot="activator" class="white--text">
            <v-icon>more_vert</v-icon>
          </v-btn>
          <v-list>
            <v-layout row>
              <v-list-tile @click="gotoCat('B8')" class="menucell">U8</v-list-tile>
              <v-list-tile class="menucell">&nbsp;</v-list-tile>
              <v-list-tile @click="gotoCat('B10')" class="menucell">B10</v-list-tile>
              <v-list-tile @click="gotoCat('G10')" class="menucell">G10</v-list-tile>
            </v-layout>
            <v-layout row>
              <v-list-tile sm3 @click="gotoCat('B12')" class="menucell">B12</v-list-tile>
              <v-list-tile sm3 @click="gotoCat('G12')" class="menucell">G12</v-list-tile>
              <v-list-tile sm3 @click="gotoCat('B14')" class="menucell">B14</v-list-tile>
              <v-list-tile sm3 @click="gotoCat('G14')" class="menucell">G14</v-list-tile>
            </v-layout>
            <v-layout row>
              <v-list-tile sm3 @click="gotoCat('B16')" class="menucell">B16</v-list-tile>
              <v-list-tile sm3 @click="gotoCat('G16')" class="menucell">G16</v-list-tile>
              <v-list-tile sm3 @click="gotoCat('B18')" class="menucell">B18</v-list-tile>
              <v-list-tile sm3 @click="gotoCat('G18')" class="menucell">G18</v-list-tile>
            </v-layout>
            <v-layout row>
              <v-list-tile sm3 @click="gotoCat('B20')" class="menucell">U20</v-list-tile>
              <v-list-tile sm3 @click="gotoCat('G20')" class="menucell">&nbsp;</v-list-tile>
              <v-list-tile sm3 @click="gotoCat('B20')" class="menucell">IMT</v-list-tile>
            </v-layout>
            <v-layout row>
              <v-list-tile sm4 @click="gotoRound('1')" class="menucell">R1</v-list-tile>
              <v-list-tile sm4 @click="gotoRound('2')" class="menucell">R2</v-list-tile>
              <v-list-tile sm4 @click="gotoRound('3')" class="menucell">R3</v-list-tile>
            </v-layout>
            <v-layout row>
              <v-list-tile sm4 @click="gotoRound('4')" class="menucell">R4</v-list-tile>
              <v-list-tile sm4 @click="gotoRound('5')" class="menucell">R5</v-list-tile>
              <v-list-tile sm4 @click="gotoRound('6')" class="menucell">R6</v-list-tile>
            </v-layout>
            <v-layout row>
              <v-list-tile sm4 @click="gotoRound('7')" class="menucell">R7</v-list-tile>
              <v-list-tile sm4 @click="gotoRound('8')" class="menucell">R8</v-list-tile>
              <v-list-tile sm4 @click="gotoRound('9')" class="menucell">R9</v-list-tile>
            </v-layout>
          </v-list>
        </v-menu>
      </div>
      <div class="hidden-sm-and-down">
        <span class="white--text">{{$t("Category")}}</span>:
        <span class="white--text" v-text="cat"></span>
        <v-menu bottom left>
          <v-btn icon slot="activator" class="white--text">
            <v-icon>arrow_drop_down</v-icon>
          </v-btn>
          <v-list>
            <v-layout row>
              <v-list-tile class="menucell" @click="gotoCat('B8')">U8</v-list-tile>
            </v-layout>
            <v-layout row>
              <v-list-tile class="menucell" @click="gotoCat('B10')">B10</v-list-tile>
              <v-list-tile class="menucell" @click="gotoCat('G10')">G10</v-list-tile>
            </v-layout>
            <v-layout row>
              <v-list-tile class="menucell" @click="gotoCat('B12')">B12</v-list-tile>
              <v-list-tile class="menucell" @click="gotoCat('G12')">G12</v-list-tile>
            </v-layout>
            <v-layout row>
              <v-list-tile class="menucell" @click="gotoCat('B14')">B14</v-list-tile>
              <v-list-tile class="menucell" @click="gotoCat('G14')">G14</v-list-tile>
            </v-layout>
            <v-layout row>
              <v-list-tile class="menucell" @click="gotoCat('B16')">B16</v-list-tile>
              <v-list-tile class="menucell" @click="gotoCat('G16')">G16</v-list-tile>
            </v-layout>
            <v-layout row>
              <v-list-tile class="menucell" @click="gotoCat('B18')">B18</v-list-tile>
              <v-list-tile class="menucell" @click="gotoCat('G18')">G18</v-list-tile>
            </v-layout>
            <v-layout row>
              <v-list-tile class="menucell" @click="gotoCat('B20')">U20</v-list-tile>
            </v-layout>
            <v-layout row>
              <v-list-tile class="menucell" @click="gotoCat('B20')">IMT</v-list-tile>
            </v-layout>
          </v-list>
        </v-menu>
        <span class="white--text">{{$t("Round")}}</span>:
        <span class="white--text" v-text="round"></span>
        <v-menu bottom left>
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
    </v-toolbar>
    <v-content class="viewcontent">
      <v-tabs light slider-color="pink" v-model="tabix">
        <v-tab class="mx-2">
          <span>{{$t("Pairings")}}</span>
        </v-tab>
        <v-tab class="mx-2">
          <span>{{$t("Standings")}}</span>
        </v-tab>
        <v-tab class="mx-2">
          <span>{{$t('Live Games')}}</span>
        </v-tab>
        <v-tab class="mx-2">
          <span>{{$t("Files")}}</span>
        </v-tab>
      </v-tabs>
      <v-tabs-items v-model="tabix">
        <v-tab-item>
          <trn-view-pairings :updateTrn="updateTrn"></trn-view-pairings>
        </v-tab-item>
        <v-tab-item>
          <trn-view-standings :updateTrn="updateTrn"></trn-view-standings>
        </v-tab-item>
        <v-tab-item>
          <trn-view-live :trn="trn"></trn-view-live>
        </v-tab-item>
        <v-tab-item>
          <trn-view-files :updateTrn="updateTrn"></trn-view-files>
        </v-tab-item>
      </v-tabs-items>
    </v-content>
    <bycco-footer />
  </v-app>



</template>

<script>
import { loadLanguageAsync } from '../util/lang'
// import { mapState } from 'vuex'
import api from '../util/api';

import Sidebar from '../components/Sidebar'
import Topbar from '../components/Topbar'
import AdCarousel from '../components/AdCarousel'
import ByccoFooter from '../components/ByccoFooter'

import TrnViewPairings from '../components/TrnViewPairings'
import TrnViewStandings from '../components/TrnViewStandings'
import TrnViewLive from '../components/TrnViewLive'
import TrnViewFiles from '../components/TrnViewFiles'

const catmapping = {
  G8: 'U8',
  B8: 'U8',
  G10: 'G10',
  B10: 'B10',
  G12: 'G12',
  B12: 'B12',
  G14: 'G14',
  B14: 'B14',
  G16: 'G16',
  B16: 'B16',
  G18: 'B18',
  B18: 'G18',
  G20: 'U20',
  B20: 'U20',
  IMT: 'IMT',
};

export default {

  components: {
    Sidebar,
    Topbar,
    ByccoFooter,
    AdCarousel,
    TrnViewPairings,
    TrnViewStandings,
    TrnViewLive,
    TrnViewFiles,
  },

data () {
    return {
      trn: {},
      updateTrn: {},
      trns: [],
      cat: 'B8',
      round: "1",
      subdrawer: false,
      tabix: 0,
      pairings:[],
      // _t: {},
      catitems: ['B8', 'G8', 'B10', 'G10', 'B12', 'G12', 'B14', 'G14',
        'B16', 'G16', 'B18', 'G18', 'B20', 'G20', 'IMT'
      ]
    }
  },
  methods: {

    gotoCat (cat) {
      console.log('Going to cat ', cat, this.trns);
      this.cat = catmapping[cat] || cat;
      this.subdrawer = false;
      this.trns.forEach(function(t){
        console.log('looping trns', t.shortname, this.cat)
        if (t.shortname == this.cat) {
          if ('id' in this.trn ) {
            this.trn = t;
            this.updateTrn = {
              trn: t,
              round: this.round
            };
          }
          else {
            api('getTopround', {
              id_trn: t.id,
            }).then(
              function(data){
                this.trn = t;
                this.round = data;
                this.updateTrn = {
                  trn: t,
                  round: this.round
                };
              }.bind(this),
              function(data) {
                console.error('failed getting topround', data);
              }
            );
          }
        }
      }.bind(this));
    },

    gotoRound (r) {
      console.log('Going to round ', r);
      this.round = r;
      this.updateTrn = {
        trn: this.trn,
        round: r
      };
    },

  },
  mounted () {
    api('getTournaments').then(
      function(data) {
        this.trns = data.trns;
        this.gotoCat(this.cat);
      }.bind(this)
    );
  },

  created () {
    loadLanguageAsync(window.config.lang);
  },
}
</script>
<style scoped>
.subtoolbar {
  margin-top: 64px !important;
}
.viewcontent {
  margin-top: 64px;
  padding-top: 1em;
}

@media  screen and (max-width: 959px)  {
  .subtoolbar {
    margin-top: 50px !important;
  }
  .viewcontent {
    margin-top: 50px;
  }
}


.menucell {
  width: 60px;
}
</style>
