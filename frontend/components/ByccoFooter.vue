<template>
<v-footer color="blue-grey lighten-1" dark class="mt-2">
  <v-container >
    <v-row class="py-3">
      <v-col class="mt-2">
        <h4 class="mb-2">{{ $t('About Bycco')}}</h4>
        <div>Belgian Youth Chess Championship Organizers. {{ $t('npo.')}}</div>
        <div>Nieuwenhovelaan 2, 02-02, <br />
            8020 Oostkamp.<br />
            e-mail: <a href="mailto:info@bycco.be">info@bycco.be</a>
        </div>
        <div>{{ $t('VAT')}}: BE 0630.723.395</div>
        <div>IBAN: BE33 0017 5924 5146</div>
      </v-col>
      <v-col class="mt-2">
        <h4 class="mb-2">{{$t('Our mission')}}</h4>
        <div class="mb-2">{{ $t('GoalBycco')}}</div>
        <div><a href="/aboutus">{{ $t('The team')}}</a></div>
      </v-col>
      <v-col class="mt-2">
        <h4 class="mb-2">Social media</h4>
        <div>
          Facebook: <a href="https://www.facebook.com/ByccoBel">
            <img style="vertical-align: middle" src="~/assets/facebook.png">
          </a>
        </div>
        <div>
          Twitter: <a href="https://twitter.com/@ByccoBel">
            <img style="vertical-align: middle" src="~/assets/twitter.png">
        </a>
        </div>
      </v-col>
    </v-row>
    <v-row>
      <v-col xs12 fluid class="text-center blue-grey darken-1 mt-3 py-2 px-1">
        Website by <a target="_blank" href="https://www.chessdevil.net">
        Chessdevil Consulting</a>. &copy; 2018 - 2021.  All rights reserved
      </v-col>
    </v-row>
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

</style>wz1knbg
