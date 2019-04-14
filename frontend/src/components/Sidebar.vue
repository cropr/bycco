<template>
    <v-navigation-drawer v-cloak dark temporary fixed v-model="drawer"
                         class="navmax blue-grey darken-1" :class="{fixtoolbar: fixtoolbar}">
      <v-toolbar flat class="blue-grey">
        <v-list>
          <v-list-tile>
            <v-list-tile-title class="title">
              Menu
            </v-list-tile-title>
          </v-list-tile>
        </v-list>
      </v-toolbar>
      <v-divider></v-divider>
      <div class="btn-language blue-grey darken-1">
        <v-btn flat class="hover-darker btn-language" :href="url_i18nn('nl')">NL</v-btn>
        <v-btn flat class="hover-darker btn-language" :href="url_i18nn('fr')">FR</v-btn>
        <v-btn flat class="hover-darker btn-language" :href="url_i18nn('de')">DE</v-btn>
        <v-btn flat class="hover-darker btn-language" :href="url_i18nn('en')">EN</v-btn>
      </div>
      <v-list dark dense class="blue-grey darken-1">
        <cms-menu-items></cms-menu-items>
        <v-list-tile href="/trn/subscription"  v-if="sections.subscription">
          <v-list-tile-content>{{$t('Register')}}</v-list-tile-content>
        </v-list-tile>
        <v-list-tile href="/trn/participants"  v-if="sections.participants">
          <v-list-tile-content>{{$t('Participants')}}</v-list-tile-content>
        </v-list-tile>
        <v-list-tile href="/trn/view"  v-if="sections.tournament">
          <v-list-tile-content>{{$t('Tournament')}}</v-list-tile-content>
        </v-list-tile>
      </v-list>
      <v-divider></v-divider>
      <v-list dark dense class="blue-grey darken-1" v-if="authenticated">
        <v-list-group>
          <v-list-tile slot="activator">
            <v-list-tile-content>Admin</v-list-tile-content>
          </v-list-tile>
          <v-list-tile href="/subscribe/mg_attendee">
            <v-list-tile-action></v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>Participants</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile href="/subscribe/mg_attendee_vue">
            <v-list-tile-action></v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>Attendee New</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile href="/subscribe/mg_presence">
            <v-list-tile-action></v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>Presence Check</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile href="/subscribe/mg_trn">
            <v-list-tile-action></v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>{{ $t('Tournament')}}</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile href="/subscribe/mg_swar">
            <v-list-tile-action></v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>SWAR management</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile href="/subscribe/printboardnumbers">
            <v-list-tile-action></v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>Print boardnumbers</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list-group>
      </v-list>
    </v-navigation-drawer>
</template>

<script>

import { mapState } from 'vuex'

export default {

  name: "Sidebar",

  computed: {
    drawer: {
      get () {
        return this.$store.state.drawer
      },
      set (value) {
        this.$store.commit('updateDrawer', value)
      }
    },
    ...mapState(['authenticated']),
  },

  data () {return {
    fixtoolbar: false,
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

  methods: {
    url_i18nn (lang) {
      return window.config.url_i18n[lang];
    }
  }


}

</script>

<style scoped>
.fixtoolbar {
  top: 50px;
}
.btn-language {
  min-width: 0;
}
</style>