<template>
  <v-app>
    <v-navigation-drawer app persistent temporary dark v-model="drawer">
      <v-list>
        <v-list-tile @click="clickedMenu('Reglement')">
          <v-list-tile-content>Reglement</v-list-tile-content>
        </v-list-tile>
        <v-list-group >
          <v-list-tile slot="item" @click="">
            <v-list-tile-content>Info</v-list-tile-content>
            <v-list-tile-action>
              <v-icon>keyboard_arrow_down</v-icon>
            </v-list-tile-action>
          </v-list-tile>
          <v-list-tile @click="clickedMenu('verblijf')">
            <v-list-tile-content>Verblijf</v-list-tile-content>
          </v-list-tile>
          <v-list-tile @click="clickedMenu('huishoud')">
            <v-list-tile-content>Huishoudelijk reglement</v-list-tile-content>
          </v-list-tile>
        </v-list-group>
      </v-list>
    </v-navigation-drawer>
    <v-toolbar app fixed class="toolbar-landing">
      <v-toolbar-side-icon @click.stop="toggleMenu()"></v-toolbar-side-icon>
      <v-toolbar-items>
        <v-btn flat large>BYC 2018</v-btn>
      </v-toolbar-items>
      <v-spacer></v-spacer>
      <v-toolbar-items class="hidden-sm-and-down">
        <v-btn flat large @click="gotoUrl('/nlinfo')">
          Lodging
        </v-btn>
        <v-btn flat large>Registration</v-btn>
        <v-btn flat large>Rules</v-btn>
      </v-toolbar-items>
    </v-toolbar>
  </v-app>
</template>

<script>

  export default {
    data () {
      return {
        drawer: false,
      }
    },
    methods: {
      toggleMenu () {
        this.drawer = !this.drawer;
      },
      gotoUrl (url) {
        console.log('going to ', url)
      },
      clickedMenu (item) {
        console.log('clicked menu', item)
      }
    }
  }

</script>

<style scoped>
.navigation-drawer {
  max-width: 85%;
}
</style>
