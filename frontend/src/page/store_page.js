import Vue from 'vue'
import Vuex from 'vuex'
import { setLanguage } from '@/util/lang'

Vue.use(Vuex);

function defaultlanguage() {
  let supportedLocales = ['en', 'fr', 'de', 'nl'];
  let pparts = window.location.pathname.split('/');
  let locale = window.localStorage.getItem('locale');
  if (!locale) {
    if (pparts.length > 3) {
      locale = pparts[3]
    }
    else {
      locale = navigator.language.split('-')[0];
    }
    if (!supportedLocales.includes(locale)) {
      locale = 'en'
    }
  }
  window.localStorage.setItem('locale', locale);
  console.log('defaultLocale', locale)
  return locale;
}

function defaultslug() {
  let pparts = window.location.pathname.split('/');
  return pparts.length > 2 ? pparts[2] : 'home';
}


const store = new Vuex.Store({
  state: {
    api: null,
    drawer: false,
    locale: defaultlanguage(),
    slug: defaultslug(),
  },

  mutations: {

    updateApi(state, payload) {
      state.api = payload;
    },

    updateDrawer (state, payload) {
      console.log('update drawer', payload)
      state.drawer = payload;
    },

    updateLocale (state, payload) {
      state.locale = payload;
      setLanguage(payload);
      window.localStorage.setItem('locale', payload);
    },

    updateSlug (state, payload) {
      state.slug = payload || state.slug;
    },

  }
})

export default store