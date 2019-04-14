<template>
<v-toolbar v-cloak fixed dark app
           class="blue-grey darken-2" :class="{fixtoolbar: fixtoolbar, landing: landing}">
  <v-toolbar-side-icon @click.stop="openDrawer"></v-toolbar-side-icon>
  <v-toolbar-items>
    <v-btn flat large href="/">{{ $t('BYC 2019')}}</v-btn>
  </v-toolbar-items>
  <v-spacer></v-spacer>
  <v-toolbar-items class="hidden-sm-and-down">
    <v-btn flat large href="/info/calendar">{{ $t('Calendar')}}
    </v-btn>
    <v-btn flat large href="/info/lodging-and-meals">{{ $t('Lodging')}}
    </v-btn>
    <v-btn flat large href="/trn/participants" v-if="sections.participants">
      {{ $t('Participants')}}
    </v-btn>
    <v-btn flat large href="/trn/subscription" v-if="sections.subscription">
      {{ $t('Register')}}
    </v-btn>
    <v-btn flat large href="/trn/view" v-if="sections.tournament">
      {{ $t('Tournament')}}
    </v-btn>
  </v-toolbar-items>
</v-toolbar>
</template>

<script>
export default {

  name: "Topbar",

  data () {return {
    fixtoolbar: false,
    landing: window.config.landing,
    sections: {
      participants: window.config.participants_enabled,
      subscription: window.config.subscriptions_enabled,
      tournament: window.config.tournament_enabled,
    },
  }},

  mounted() {
    if (window.CMS) {
      this.fixtoolbar = true;
    }
  },

  methods:   {
    openDrawer () {
      this.$store.commit('updateDrawer', true)
    },
    url_i18nn (lang) {
      return window.config.url_i18n[lang];
    }
  },
}
</script>

<style scoped>
.fixtoolbar {
  top: 50px;
}

.landing.blue-grey.darken-2 {
  background-color: rgba(77, 94, 101, 0.4) !important;
  /*background-color: green;*/
}
</style>