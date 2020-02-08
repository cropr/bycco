import Vue from 'vue'
import Vuex from 'vuex'
import { setLanguage } from '@/util/lang'
import { getPageContent } from '@/util/page'
import { getDocContent } from '@/util/docpage'

Vue.use(Vuex);

function defaultlanguage(){
  let supportedLocales = ['en', 'fr', 'de', 'nl'];
  let l = window.config.locale;
  l = l || window.localStorage.getItem('locale');
  l = l || navigator.language.split('-')[0]; 
  if (! supportedLocales.includes(l)) {
    l = 'en'
  } 
  window.localStorage.setItem('locale', l);
  return l;  
}

const initflow = {
  category: '',
  emailplayer: '',
  emailparent: '',
  fullnameattendant: '',
  fullnameparent: '',
  hasAgreedNat: false,
  hasAgreedPriv: false,
  idnumber: '',
  isConfirmed: false,
  isParentPresent: true,
  isPlayerFound: false,
  mobileplayer: '',
  mobileattendant: '',
  mobileparent: '',
  step: 1,
};

const store = new Vuex.Store({
  state: {
    doc: {},
    drawer: false,
    flow: initflow,
    locale: defaultlanguage(),
    page: {},
    photo: '',
    slug: null,  
    subscription: {},
  },

  mutations: {

    // drawer
    updateDrawer (state, payload) {
      console.log('update drawer', payload)
      state.drawer = payload;
    },

    // page
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

    // doc
    updateDocUrl (state, payload) {
      state.locale = payload.locale || state.locale;
      state.slug = payload.slug || state.slug;
      window.localStorage.setItem('locale', state.locale);
      console.log('check 204')    
      setLanguage(state.locale);
      getDocContent();
    },
    updateDoc (state, payload) {
      console.log('check 203')    
      state.doc = payload;
    },


    // locale
    updateLocale (state, payload) {
      state.locale = payload || state.locale;
      window.localStorage.setItem('locale', state.locale);
      setLanguage(state.locale);
    },

    // subscription
    delSubscription(state){
      state.subscription = {}
    },
    setSubscription(state, player) {
      state.subscription = player;
    },
    updateSubscription(state, player){
      state.subscription = Object.assign({}, state.subscription, player)
    },
    setPhoto (state, payload) {
      state.photo = payload
    },
    init (state) {
      console.log('calling init', state)
      state.flow = initflow;
      state.subscription = {};
      state.photo = '';
      console.log('after init', state)
    },
    updateFlow(state, payload){
      state.flow = Object.assign({}, state.flow, payload)
    },

  }
})

export default store