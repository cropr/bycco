<template>
<div class="mt-2">
 <v-card v-show="pdfgames" class="ma-2">
   <v-card-title>
     <h4>Available files to download</h4>
   </v-card-title>
   <p class="mt-3 ml-2">PDF</p>
   <ul v-for="p in pdfgames" :key="p.filename">
     <li class="my-1"><a :href="'/media/' + p.file" v-text="p.filename"></a></li>
   </ul>
   <p class="mt-3 ml-2">PGN</p>
   <ul v-for="p in pgngames" :key="p.filename">
     <li class="my-1"><a :href="'/media/' + p.file" v-text="p.filename"></a></li>
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
      // var self=this;
      // this.pdfgames = [];
      // api('getPdfGames', {
      //   id_trn: this.trn.id,
      // }).then(
      //   function(data){
      //     self.pdfgames = data.pdfgames;
      //   },
      //   function(data) {
      //     console.error('failed getting pdfgames', data);
      //   }
      // );
    },
    getPgnGames () {
      // var self=this;
      // this.pgngames = [];
      // api('getPgnGames', {
      //   id_trn: this.trn.id,
      // }).then(
      //   function(data){
      //     self.pgngames = data.pgngames;
      //   },
      //   function(data) {
      //     console.error('failed getting pgngames', data);
      //   }
      // );
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
