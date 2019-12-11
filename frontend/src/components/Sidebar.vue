<template>
  <v-navigation-drawer app v-model="drawer" dark v-cloak
      class="navmax blue-grey darken-1" >
    <v-toolbar text class="blue-grey">
      <v-list>
        <v-list-item>
          <v-list-item-title class="title">
            Menu
          </v-list-item-title>
        </v-list-item>
      </v-list>
    </v-toolbar>
    <v-divider></v-divider>
    <div class="btn-language blue-grey darken-1">
      <v-btn text class="hover-darker btn-language" @click="updateLocale('nl')">NL</v-btn>
      <v-btn text class="hover-darker btn-language" @click="updateLocale('fr')">FR</v-btn>
      <v-btn text class="hover-darker btn-language" @click="updateLocale('de')">DE</v-btn>
      <v-btn text class="hover-darker btn-language" @click="updateLocale('en')">EN</v-btn>
    </div>
    <v-list dark dense class="blue-grey darken-1">
      <v-list-item @click="updateSlug('home')" >
          <v-list-item-icon>
            <v-icon>home</v-icon>
          </v-list-item-icon>
        <v-list-item-content>{{$t('Home')}}</v-list-item-content>
      </v-list-item>
      <v-list-group no-action>
          <template v-slot:activator>
            <v-list-item-icon>
              <v-icon>info</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Info</v-list-item-title>
            </v-list-item-content>
          </template>
          <v-list-item @click="updateSlug('toernooireglement')" >
            <v-list-item-content>{{$t('Tournament Rules')}}</v-list-item-content>
          </v-list-item>
          <v-list-item @click="updateSlug('huisreglement')" >
            <v-list-item-content>{{$t('Internal Regulations')}}</v-list-item-content>
          </v-list-item>
          <v-list-item @click="updateSlug('verblijf')" >
            <v-list-item-content>{{$t('Lodging')}}</v-list-item-content>
          </v-list-item>
          <v-list-item @click="updateSlug('toewijzingverblijf')" >
            <v-list-item-content>{{$t('Lodging Allocation')}}</v-list-item-content>
          </v-list-item>
          <v-list-item @click="updateSlug('restaurant')" >
            <v-list-item-content>{{$t('Catering')}}</v-list-item-content>
          </v-list-item>
      </v-list-group>

      <v-list-item href="/subscription">
          <v-list-item-icon>
            <v-icon>subscriptions</v-icon>
          </v-list-item-icon>      
        <v-list-item-content>{{ $t('Register') }}</v-list-item-content>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script>

import { navigation } from '@/util/utils'

export default {

  name: "Sidebar",

  data () {return {
    sections: {
      participants: false, // window.config.participants_enabled,
      subscription: false, // window.config.subscriptions_enabled,
      tournament: false, //window.config.tournament_enabled,
    },

  }},

  computed: {
    drawer: {
      get () {
        return this.$store.state.drawer
      },
      set (value) {
        this.$store.commit('updateDrawer', value)
      }
    },
  },

  mounted() {
  },

  methods: {
    updateLocale: function(l){
      navigation.changeLocale(l)
    },
    updateSlug: function(l){
      navigation.changeSlug(l)
    },
  }

}

</script>

<style scoped>
.btn-language {
  min-width: 0;
}
.v-list-group--active.primary--text {
  color: white !important;
}
</style>