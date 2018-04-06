<template>
<div>
 <v-toolbar color="blue-grey lighten-2">
   <v-toolbar-title>
     <h3 class="white--text">Tournament Results</h3>
   </v-toolbar-title>
   <v-spacer></v-spacer>
   <v-btn flat color="white">
     <v-icon>more_vert</v-icon>
   </v-btn>
 </v-toolbar>
</div>
</template>

<script>
import api from '../api/api';

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
  },
  data () {
    return {
      trns: [],
      cat: 'G8',
      round: 1,
    }
  },
  methods: {

  },
  mounted () {

  },
}
</script>

<style>
</style>
