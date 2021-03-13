export default {
  target: 'static',

  head: {
    titleTemplate: '%s - Bycco',
    title: 'bycco',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
    ],
    link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }],
  },

  css: [],

  plugins: [{ src: '~plugins/markdown-it-vue', ssr: false }],

  components: true,

  buildModules: ['@nuxtjs/vuetify'],

  modules: ['@nuxtjs/axios', '@nuxtjs/pwa', 'nuxt-i18n'],

  axios: {},

  pwa: {
    manifest: {
      lang: 'en',
    },
  },

  vuetify: {
    customVariables: ['~/assets/variables.scss'],
    theme: {
      light: true,
      // themes: {
      //   dark: {
      //     primary: colors.blue.darken2,
      //     accent: colors.grey.darken3,
      //     secondary: colors.amber.darken3,
      //     info: colors.teal.lighten1,
      //     warning: colors.amber.base,
      //     error: colors.deepOrange.accent4,
      //     success: colors.green.accent3,
      //   },
      // },
    },
  },

  build: {},

  i18n: {
    lazy: true,
    locales: [
      { code: 'nl', file: 'nl.js' },
      { code: 'fr', file: 'fr.js' },
      { code: 'de', file: 'de.js' },
      { code: 'en', file: 'en.js' },
    ],
    langDir: 'lang/',
    strategy: 'prefix',
    defaultLocale: 'nl',
  },
}
