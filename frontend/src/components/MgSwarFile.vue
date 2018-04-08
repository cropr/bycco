<template>
<div>
  <v-card class="ma-2">
    <v-card-title>
      <h4>Pairings</h4>
    </v-card-title>
    <v-card-text>
      <table style="width:auto;">
        <tr v-for="(p,ix) in pairings" :key="p.white">
          <td v-text="ix + 1"></td>
          <td v-text="p.white"></td>
          <td v-text="p.result"></td>
          <td v-text="p.black"></td>
        </tr>
        <tr v-show="bye">
          <td></td>
          <td v-text="bye.white"></td>
          <td>Bye</td>
          <td></td>
        </tr>
        <tr v-for="p in absences" :key="p.white">
          <td></td>
          <td v-text="p.white"></td>
          <td>Abs.</td>
          <td></td>
        </tr>
      </table>
    </v-card-text>
    <v-card-actions>
      <v-btn color="primary" @click="printPairing">Print</v-btn>
    </v-card-actions>
  </v-card>
  <v-card class="ma-2">
    <v-card-title>
      <h4>Standings</h4>
    </v-card-title>
    <v-card-text>
      <table style="width:auto;">
        <tr v-for="(p,ix) in players" :key="p.name">
          <td v-text="ix + 1"></td>
          <td v-text="p.name"></td>
          <td v-text="p.points"></td>
        </tr>
      </table>
    </v-card-text>
    <v-card-actions>
      <v-btn color="primary" @click="printStanding">Print</v-btn>
    </v-card-actions>
  </v-card>

</div>
</template>

<script>
import _ from 'lodash';

export default {
  props: ['swarfile'],
  data () {
    return {
      pairings: [],
      bye: {},
      absences: [],
      players: [],
    }
  },
  methods: {
    parseSwarFile () {
      var players, six, pix, pl, lastgame, absences = [], bye, self=this;
      var swarjsonfile = JSON.parse(self.swarfile.jsonfile).Swar;
      players = swarjsonfile.Player;
      self.pairings = [];
      self.absences = [];
      self.bye = {};
      self.players = [];
      _.forEach(players, function(p) {
        six = p.Ranking - 1;
        pl = {
          name: p.Name,
          playerindex: p.Ni,
          points: parseFloat(p.Points),
          gender: (p.Sex == 'Male' ? 'M' : 'F' ),
          country: p.Country,
          id_national: p.NationalId + '',
          id_fide: p.FideId + '',
          id_club: p.ClubNumber + '',
          clubname: p.ClubName,
          natrating: p.NationalElo,
          fiderating: p.FideElo,
          titel: p.Titel,
          ngames: p.NbofParts,
          games: [],
          bye: null,
          absences: []
        };
        _.forEach(p.RoundArray, function(g, ix) {
          if (g.Tabel == "Absent") {
            pl.absences.push({
              round: g.RoundNr - 1
            });
            if (ix == p.RoundArray.length - 1) {  // current Round
              self.absences.push({
                white: pl.name,
                result: '--'
              });
            }
            self.players[six] = pl;
            return;
          }
          if (g.Tabel == 'BYE') {
            pl.bye = {
              round: g.RoundNr - 1
            };
            if (ix == p.RoundArray.length - 1) {  // current Round
              self.bye = {
                white: pl.name,
                result: 'Bye'
              }
            }
            self.players[six] = pl;
            return;
          }
          lastgame = {
            table: parseInt(g.Tabel) - 1,
            opponentIndex: g.OpponentNi,
            opponentName: g.OpponentName,
            result: g.Result,
            color: (g.Color == "Black" ? 'B' : 'W'),
            float: g.Float,
            round: g.RoundNr
          };
          pl.games.push(lastgame);
          if (ix == p.RoundArray.length - 1) {  // current Round
            pix = lastgame.table;
            if (!self.pairings[pix]) self.pairings[pix] = {};
            if (lastgame.color == 'W') {
              self.pairings[pix].white = pl.name;
              self.pairings[pix].black = lastgame.opponentName;
              switch (lastgame.result.toUpperCase()) {
                case '1':
                  self.pairings[pix].result = '1-0';
                  break;
                case '½':
                  self.pairings[pix].result = '½-½';
                  break;
                case '0':
                  self.pairings[pix].result = '0-1';
                  break;
                case '1FF':
                  self.pairings[pix].result = '1-0 FF';
                  break;
                case '0FF':
                  self.pairings[pix].result = '0-1 FF';
                  break;
              }
            }
          }
          self.players[six] = pl;
        });
      });
    },
    printPairing () {
      window.open('/subscribe/printpairing?id_swarfile='+this.swarfile.id, '_blank')
    },
    printStanding () {

    },
  },
  watch: {
    swarfile: function(newVal, oldVal) {
      if ('jsonfile' in newVal) {
        this.parseSwarFile();

      }
    }
  }

}
</script>

<style scoped>
</style>
