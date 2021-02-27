<template>
  <div>
    <v-toolbar text class="blue-grey">
      <v-list>
        <v-list-item>
          <v-list-item-title class="title"> Menu </v-list-item-title>
        </v-list-item>
      </v-list>
    </v-toolbar>
    <v-divider></v-divider>
    <div class="btn-language blue-grey darken-1">
      <v-btn text class="hover-darker btn-language" @click="updateLocale('nl')"
        >NL</v-btn
      >
      <v-btn text class="hover-darker btn-language" @click="updateLocale('fr')"
        >FR</v-btn
      >
      <v-btn text class="hover-darker btn-language" @click="updateLocale('de')"
        >DE</v-btn
      >
      <v-btn text class="hover-darker btn-language" @click="updateLocale('en')"
        >EN</v-btn
      >
    </div>
    <v-list dark dense class="blue-grey darken-1">
      <v-list-item @click="updateSlug('home')">
        <v-list-item-icon>
          <v-icon>home</v-icon>
        </v-list-item-icon>
        <v-list-item-content>{{ $t('Home') }}</v-list-item-content>
      </v-list-item>
      <v-list-group no-action>
        <template v-slot:activator>
          <v-list-item-content>
            <v-list-item-title>Info</v-list-item-title>
          </v-list-item-content>
        </template>
        <v-list-item @click="updateSlug('toernooireglement')">
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
        <template v-slot:activator>
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
