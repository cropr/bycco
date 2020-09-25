<template>
<v-app-bar v-cloak dark app class="blue-grey darken-2" 
    :class="{landing: landing}">
  <v-app-bar-nav-icon @click.stop="toggleDrawer" />
  <v-toolbar-items>
    <v-btn text large href="/">{{ $t('BYC 2020')}}</v-btn>
  </v-toolbar-items>
  <v-spacer></v-spacer>
  <v-toolbar-items class="hidden-sm-and-down">
    <!-- <v-btn text large href="/participants">
      {{ $t('Participants')}}
    </v-btn> -->
    <v-btn text large @click="updateSlug('subscription')" >
      {{ $t('Enrollment')}}
    </v-btn>
    <!-- <v-btn text large href="/trn" >
      {{ $t('Tournament')}}
    </v-btn> -->
  </v-toolbar-items>
</v-app-bar>
</template>

<script>
import { mapState } from 'vuex'

export default {

  name: "Topbar",

  computed: {
    ...mapState(['drawer', 'locale']),
  },

data () {return {
    fixtoolbar: false,
    landing: true, //window.config.landing,
    sections: {
      participants: false, //window.config.participants_enabled,
      tournament: false, //window.config.tournament_enabled,
    },
  }},


  methods:   {

    toggleDrawer () {
      this.$store.commit('updateDrawer', !this.drawer)
    },
    
    updateSlug: function(s){
      this.$router.push('/page/'+ s + '/' + this.locale)
    },

    url_i18n (lang) {
      return '/' + lang // window.config.url_i18n[lang];
    },

  },
}
</script>

<style scoped>

.landing.blue-grey.darken-2 {
  background-color: rgba(77, 94, 101, 0.4) !important;
}
</style>