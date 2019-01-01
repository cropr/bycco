<template>
<v-footer height="auto" color="blue-grey lighten-1" dark class="mt-2">
  <v-container>
    <v-layout row wrap class="py-3">
      <v-flex sm3 xs12 class="mt-2">
        <h4 class="mb-2">{{ $t('About Bycco')}}</h4>
        <div>Belgian Youth Chess Championship Organizers. {{ $t('npo.')}}</div>
        <div>Museumstraat 67<br>
           9881 Bellem<br>
           e-mail: <a href="mailto:info@bycco.be">info@bycco.be</a>
        </div>
        <div>{{ $t('VAT')}}: BE 0630.723.395</div>
      </v-flex>
      <v-flex sm5 offset-sm1 xs12 class="mt-2">
        <h4 class="mb-2">{{$t('Our mission')}}</h4>
        <div class="mb-2">{{ $t('GoalBycco')}}</div>
        <div><a href="/us/organizers">{{ $t('The organizers')}}</a></div>
        <div><a href="/us/arbiters">{{ $t('The arbiters')}}</a></div>
      </v-flex>
      <v-flex sm2 offset-sm1 xs12 class="mt-2">
        <h4 class="mb-2">Social media</h4>
        <div>
         Facebook: <a href="https://www.facebook.com/ByccoBel">
           <img style="vertical-align: middle" src="/static/img/facebook.png">
         </a>
        </div>
        <div>
          Twitter: <a href="https://twitter.com/@ByccoBel">
            <img style="vertical-align: middle" src="/static/img/twitter.png">
        </a>
        </div>
      </v-flex>
      <v-flex xs12 fluid class="text-xs-center blue-grey darken-1 mt-3 py-2 px-1">
        Website by <a target="_blank" href="https://www.chessdevil.net">
        Chessdevil Consulting</a>. &copy; 2018 - 2019.  All rights reserved
      </v-flex>
    </v-layout>
  </v-container>
</v-footer>
</template>

<script>
  export default {
    name: "ByccoFooter"
  }
</script>

<style scoped>

a {
 color: white;
}

a:link, a:hover {
  color: white;
  text-decoration: none;
}

a:hover {
  font-weight: 700;
}

</style>