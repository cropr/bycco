<template>
<div class="mt-2">
 <v-card v-show="pdfgames" class="ma-2">
   <v-card-title>
     <h4>Available files to download</h4>
   </v-card-title>
   <ul v-for="p in pdfgames" :key="p.filename">
     <li class="my-1"><a :href="'/media/' + p.file" v-text="p.filename"></a></li>
   </ul>
 </v-card>
 <div v-show="!pdfgames">
   No files available yet
 </div>
</div>
</template>

<script>

import api from '../api/api';

export default {
  props: ['updateTrn'],
  data () {
    return {
      pdfgames: [],
    }
  },
  methods: {
    getPdfGames () {
      var self=this;
      api('getPdfGames', {
        id_trn: this.trn.id,
      }).then(
        function(data){
          self.pdfgames = data.pdfgames;
        },
        function(data) {
          console.error('failed getting pdfgames', data);
        }
      );
    }
  },
  watch: {
    updateTrn: function (newVal, oldVal) {
      this.trn = newVal.trn;
      this.getPdfGames();
    },
  }
}
</script>

<style>
</style>
