<template>
<div class="mt-2">
 <v-card v-show="pdfgames" class="ma-2">
   <v-card-title>
     <h4>Available files to download</h4>
   </v-card-title>
   <p class="mt-3 ml-2">PDF</p>
   <ul v-for="p in pdfgames" :key="p.filename">
     <li class="my-1"><a :href="'/media/' + p.file" v-text="p.beautyname"></a></li>
   </ul>
   <p class="mt-3 ml-2">PGN</p>
   <ul v-for="p in pgngames" :key="p.filename">
     <li class="my-1"><a :href="'/media/' + p.file" v-text="p.beautyname"></a></li>
   </ul>
   <br>
 </v-card>
 <div v-show="!pdfgames">
   No files available yet
 </div>
</div>
</template>

<script>

import api from '../util/api';

export default {
  props: ['updateTrn'],
  data () {
    return {
      pdfgames: [],
      pgngames: [],
    }
  },
  methods: {
    getPdfGames () {
      this.pdfgames = [];
      api('getPdfGames', {
        id_trn: this.trn.id,
      }).then(
        function(data){
          this.pdfgames = data.pdfgames;
          this.pdfgames.forEach(function(p){
            var name = p.filename.split('.')[0];
            var catround = name.split('_')[1].split('R');
            p.beautyname = catround[0] + ' round ' + catround[1]
          }.bind(this));
        }.bind(this),
        function(data) {
          console.error('failed getting pdfgames', data);
        }
      );
    },
    getPgnGames () {
      this.pgngames = [];
      api('getPgnGames', {
        id_trn: this.trn.id,
      }).then(
        function(data){
          this.pgngames = data.pgngames;
          this.pgngames.forEach(function(p){
            var catround = p.filename.split('.')[0].split('R');
            p.beautyname = catround[0] + ' round ' + catround[1]
          })
        }.bind(this),
        function(data) {
          console.error('failed getting pgngames', data);
        }
      );
    }
  },
  watch: {
    updateTrn: function (newVal) {
      this.trn = newVal.trn;
      this.getPdfGames();
      this.getPgnGames();
    },
  }
}
</script>

<style>
</style>
