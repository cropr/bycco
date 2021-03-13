<template>
  <v-container>
    <h1>{{ title[$i18n.locale] }}</h1>
    <hr />
    <markdown-it-vue class="md-body mt-2" :content="content[$i18n.locale]" />
  </v-container>
</template>

<script>
export default {
  layout: 'landing',

  data() {
    return {
      title: {
        en: 'Announcement Belgian Youth Chess Championships 2021',
        nl: 'Aankondiging Belgische Jeugdkampioenschappen Schaken 2021',
        fr: "Annonce des Championnats de Belgique d'échecs de la jeunesse 2021",
        de: 'Ankündigung der belgischen Jugendschachmeisterschaften 2021',
      },
      content: {
        en: `The Championships 2021 will take place during the prolonged 
weekend of 11th till 14th November 2021 in the Floreal in Blankenberge.

More information will be announced in March`,
        nl: `De kampioenschappen 2021 vinden plaats tijdens het verlengde 
weekend van 11 t / m 14 november 2021 in de Floreal in Blankenberge

Meer informatie wordt in maart bekend gemaakt`,
        fr: `Les Championnats 2021 auront lieu pendant le week-end prolongé 
du 11 au 14 novembre 2021 au Floreal de Blankenberge

Plus d'informations seront annoncées plus en mois de mars`,
        de: `Die Meisterschaften 2021 finden am verlängerten Wochenende 
vom 11. bis 14. November 2021 im Floreal in Blankenberge statt

Weitere Informationen werden im März bekannt gegeben`,
      },
    }
  },

  head: {
    title: 'Belgian Youth Chess Championships 2021',
    titleTemplate: '%s - BYCCO',
    link: [
      {
        rel: 'stylesheet',
        href:
          'https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900',
      },
      {
        rel: 'stylesheet',
        href: 'https://fonts.googleapis.com/css?family=Material+Icons',
      },
      {
        rel: 'stylesheet',
        href:
          'https://cdn.jsdelivr.net/npm/@mdi/font@latest/css/materialdesignicons.min.css',
      },
      { rel: 'favicon', href: 'favicon.ico' },
    ],
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'home', name: 'description', content: 'Meta description' },
    ],
    script: [
      {
        src: 'https://apis.google.com/js/platform.js',
        async: true,
        defer: true,
      },
    ],
  },
}
</script>
