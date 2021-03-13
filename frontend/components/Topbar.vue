<template>
  <v-app-bar
    v-cloak
    dark
    app
    class="blue-grey darken-2"
    :class="{ landing: landing }"
  >
    <v-app-bar-nav-icon @click="toggleDrawer" />
    <v-toolbar-items>
      <v-btn text large :to="localePath('index')">{{ $t('BYC 2020') }}</v-btn>
    </v-toolbar-items>
    <v-spacer></v-spacer>
    <v-toolbar-items class="hidden-sm-and-down">
      <!-- <v-btn text large href="/participants">
      {{ $t('Participants')}}
    </v-btn> -->
      <v-btn text large @click="updateSlug('subscription')">
        {{ $t('Enrollment') }}
      </v-btn>
      <!-- <v-btn text large href="/trn" >
      {{ $t('Tournament')}}
    </v-btn> -->
    </v-toolbar-items>
  </v-app-bar>
</template>

<script>
export default {
  name: 'Topbar',

  props: {
    landing: {
      type: String,
      default: null,
    },
    drawer: {
      type: Boolean,
      default: null,
    },
  },

  methods: {
    toggleDrawer() {
      this.$emit('updateDrawer', !this.drawer)
    },
  },
}
</script>

<style scoped>
.landing.blue-grey.darken-2 {
  background-color: rgba(77, 94, 101, 0.4) !important;
}
</style>
