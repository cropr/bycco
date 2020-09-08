import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    api: null,
    drawer: false, 
    token: window.localStorage.getItem('websitetoken'),
    page: {},
    participant: {},
    printselection: [],
    routebeforelogin: '',
  },

  mutations: {
    updateApi(state, payload) {
      state.api = payload;
    },
    updateDrawer (state, payload) {
      state.drawer = payload;
    },
    updateToken (state, payload) {
      state.token = payload;
      window.localStorage.setItem('websitetoken', payload)
    },
    updatePage (state, payload) {
      state.page = payload;
    },
    updateParticipant (state, payload) {
      state.participant = payload;
    },
    updatePrintSelection(state, payload) {
      state.printselection = payload;
    },
    updateRouteBeforeLogin (state, payload) {
      state.routebeforelogin = payload;
    },
  }
})

export default store