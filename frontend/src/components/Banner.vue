<template>
<div>
  <v-parallax src="/static/img/pier_big.jpg" height="350" >

  </v-parallax>
  <div class="landing-title">
    {{ $t("Belgian Youth Chess Championships 2019") }}
  </div>
</div>
</template>

<script>
export default {
  name: "Banner"
}
</script>

<style scoped>
.landing-box {
  background-position: center top;
  background-size: auto 100%;
  background-repeat: no-repeat;
  width: auto;
  position: relative;
}

.landing-title {
  position: absolute;
  top: 80px;
  right: 1em;
  font-size: 200%;
  color: #b9cbe7;
  padding: 0.5em 1em;
  background-color: rgba(33, 39, 41, 0.35);
}

/*@media screen and (min-width: 1281px) {*/
  /*.landing-box{*/
    /*height: 524px;*/
    /*background-image: url('/static/img/landing_big.jpeg')*/

  /*}*/
/*}*/

/*@media screen and (min-width: 720px) and (max-width: 1280px) {*/
  /*.landing-box {*/
    /*height: 349px;*/
    /*background-image: url('/static/img/landing_medium.jpeg');*/
  /*}*/
  /*.landing-title {*/
    /*font-size: 150%*/
  /*}*/
/*}*/

/*@media screen and (max-width: 720px) {*/
  /*.landing-box{*/
    /*height: 196px;*/
    /*background-image: url('/static/img/landing_small.jpeg');*/
  /*}*/
  /*.landing-title {*/
    /*font-size: 100%;*/
  /*}*/
/*}*/


</style>