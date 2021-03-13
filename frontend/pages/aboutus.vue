<template>
  <v-container>
    <h1>{{ title[$i18n.locale] }}</h1>
    <hr />
    <markdown-it-vue class="md-body mt-2" :content="content[$i18n.locale]" />
  </v-container>
</template>

<script>
export default {
  layout: 'default',

  data() {
    return {
      title: {
        en: 'About Bycco',
        nl: 'Over Bycco',
        fr: 'Comcernant Bycco',
        de: 'Über Bycco',
      },
      content: {
        en: `To Do`,
        nl: `Te doen`,
        fr: `A faire`,
        de: `Zu machen`,
      },
    }
  },

  head: {
    title: 'Bycco',
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
