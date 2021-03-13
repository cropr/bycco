<template>
  <div>
    <v-toolbar dark text class="blue-grey">
      <v-list>
        <v-list-item>
          <v-list-item-title class="title"> Menu </v-list-item-title>
        </v-list-item>
      </v-list>
    </v-toolbar>
    <v-divider></v-divider>
    <div class="blue-grey darken-1">
      <v-btn text class="hover-darker btn-language" :to="switchLocalePath('nl')"
        >NL</v-btn
      >
      <v-btn text class="hover-darker btn-language" :to="switchLocalePath('fr')"
        >FR</v-btn
      >
      <v-btn text class="hover-darker btn-language" :to="switchLocalePath('de')"
        >DE</v-btn
      >
      <v-btn text class="hover-darker btn-language" :to="switchLocalePath('en')"
        >EN</v-btn
      >
    </div>
    <v-list dark dense class="blue-grey darken-1">
      <v-list-item :to="localePath('index')">
        <v-list-item-icon>
          <v-icon>home</v-icon>
        </v-list-item-icon>
        <v-list-item-content>{{ $t('Home') }}</v-list-item-content>
      </v-list-item>
      <v-list-group no-action>
        <template #activator>
          <v-list-item-content>
            <v-list-item-title>Info</v-list-item-title>
          </v-list-item-content>
        </template>
        <v-list-item :to="localePath('toernooireglement')">
          <v-list-item-content>{{
            $t('Tournament Rules')
          }}</v-list-item-content>
        </v-list-item>
        <v-list-item @click="updateSlug('huishoudreglement')">
          <v-list-item-content>
            {{ $t('Internal Regulations') }}
          </v-list-item-content>
        </v-list-item>
        <v-list-item @click="updateSlug('agenda')">
          <v-list-item-content>{{ $t('Calendar') }}</v-list-item-content>
        </v-list-item>
        <v-list-item @click="updateSlug('toernooiinfo')">
          <v-list-item-content>
            {{ $t('Important information') }}
          </v-list-item-content>
        </v-list-item>
        <v-list-item @click="updateSlug('covid19')">
          <v-list-item-content>Covid-19</v-list-item-content>
        </v-list-item>
      </v-list-group>
      <v-list-group no-action>
        <template #activator>
          <v-list-item-content>
            <v-list-item-title>{{ $t('Tournament') }}</v-list-item-title>
          </v-list-item-content>
        </template>
        <v-list-item @click="updateSlug('subscription')">
          <v-list-item-content>{{ $t('Enrollment') }}</v-list-item-content>
        </v-list-item>
        <v-list-item @click="updateSlug('participants')">
          <v-list-item-content>{{ $t('Participants') }}</v-list-item-content>
        </v-list-item>
      </v-list-group>
    </v-list>
  </div>
</template>

<script>
export default {
  name: 'Sidebar',

  methods: {
    updateLocale(l) {
      console.log('updateLocale: ', l)
    },
    updateSlug(s) {
      console.log('updateSlug: ', s)
    },
  },
}
</script>

<style scoped>
.btn-language.v-btn {
  min-width: 0;
  color: white;
}
.v-list-group--active.primary--text {
  color: white !important;
}
</style>
