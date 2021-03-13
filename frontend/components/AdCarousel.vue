<template>
<div>
  <v-card class="my-2 mx-auto" max-width="400">
    <v-card-title>Gold Sponsor:</v-card-title>
    <v-card-text>
      <a href="http://www.cronos.be" target="_blank">
      <img src='~/assets/frame_chronos.png'>
      </a>
    </v-card-text>
  </v-card>
<v-carousel :show-arrows="false" hide-delimiters :value="current" height="170"
            class="adcarousel mb-2" :interval="interval*1000" cycle continuous>
  <v-carousel-item v-for="item in items" :key="item.name" :src="item.src">
  </v-carousel-item>
</v-carousel>
</div>
</template>

<script>
export default {
  data () {
    return {
      current: 0,
      interval: 6, // number of seconds before switching
      items: [
        {src: require('~/assets/frame_archery.png'), name: 'archery' },
        // {src:'/img/frame_blankenberge.png', name: 'blankenberge' },
        {src: require('~/assets/frame_chessconsult.png'), name: 'chessconsult' },
        {src: require('~/assets/frame_cvwarehouse.png'), name: 'cvwarehouse' },
        {src: require('~/assets/frame_talistro.png'), name: 'talistro' },
      ]
    }
  },
  mounted () {
    var secCarousel = Math.floor((new Date()/1000) % (this.interval * this.items.length));
    this.current = Math.floor(secCarousel / this.items.length);
    if (this.current == this.items.length) this.current = 0;
  }
}
</script>

<style scoped>
.adcarousel.v-carousel {
  width: 360px;
  max-width: 95%;
  margin-left: auto;
  margin-right: auto;
}
</style>
