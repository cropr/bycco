import Vue from 'vue'
import Vuex from 'vuex'
import { setLanguage, locales } from '@/util/server_injected'

Vue.use(Vuex);

function defaultlanguage() {
  let pparts = window.location.pathname.split('/');
  let locale = window.localStorage.getItem('locale');
  if (!locale) {
    if (pparts.length > 3) {
      locale = pparts[3]
    }
    else {
      locale = navigator.language.split('-')[0];
    }
    if (!locales.includes(locale)) {
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

const initflow = {
  birthyear: '',
  idbel: '',
  idSubscription: null,
  isConfirmed: false,
  step: 1,
};

const store = new Vuex.Store({
  state: {
    age: 0,
    api: null,
    drawer: false,
    flow: initflow,
    locale: defaultlanguage(),
    slug: defaultslug(),
    subscription: {},
  },

  mutations: {

    init(state) {
      state.flow = initflow;
      state.subscription = {};
      state.age = 0;
    },

    updateApi(state, payload) {
      state.api = payload;
    },

    updateDrawer (state, payload) {
      state.drawer = payload;
    },

    updateFlow(state, payload){
      state.flow = Object.assign({}, state.flow, payload)
    },

    updateLocale (state, payload) {
      state.locale = payload;
      setLanguage(payload);
      window.localStorage.setItem('locale', payload);
    },

    updateSlug (state, payload) {
      state.slug = payload || state.slug;
    },

    updateSubscription(state, sub){
      state.subscription = Object.assign({}, state.subscription, sub);
      state.age = state.subscription.category ? 
        parseInt(state.subscription.category.substr(1,3)) : 0;
    },

  }
})

export default store