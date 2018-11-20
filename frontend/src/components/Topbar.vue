<template>
<v-toolbar v-cloak fixed dark app
           class="blue-grey darken-2" :class="{fixtoolbar: fixtoolbar}">
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
    <v-btn flat large href="/subscribe" v-if="subscriptions_enabled">
      {{ $t('Register')}}
    </v-btn>
    <v-btn flat large href="/bycco/subscriptions" v-if="tournament_enabled">
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
    subscriptions_enabled: window.config.subscriptions_enabled,
    tournament_enabled: window.config.tournament_enabled,
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
    urlI18n (lang) {
      return window.config.urli18[lang];
    }
  },
}
</script>

<style scoped>
.fixtoolbar {
  top: 50px;
}
</style>