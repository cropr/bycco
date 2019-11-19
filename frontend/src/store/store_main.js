import Vue from 'vue'
import Vuex from 'vuex'
import { setLanguage } from '@/util/lang'
import { getPageContent } from '@/util/page'

Vue.use(Vuex);

function defaultlanguage(){
  let supprtedLocales = ['en', 'fr', 'de', 'nl'];
  let l = window.config.locale;
  l = l || window.localStorage.getItem('locale');
  l = l || navigator.language.split('-')[0]; 
  if (! supprtedLocales.includes(l)) {
    l = 'en'
  } 
  window.localStorage.setItem('locale', l);
  return l;  
}

const store = new Vuex.Store({
  state: {
    page: {},
    locale: defaultlanguage(),
    slug: null,  
    drawer: false,
  },

  mutations: {
    updateDrawer (state, payload) {
      console.log('update drawer', payload)
      state.drawer = payload;
    },
    updatePageUrl (state, payload) {
      state.locale = payload.locale || state.locale;
      state.slug = payload.slug || state.slug;
      window.localStorage.setItem('locale', state.locale);
      setLanguage(state.locale);
      getPageContent();
    },
    updatePage (state, payload) {
      state.page = payload;
    },
  }
})

export default store