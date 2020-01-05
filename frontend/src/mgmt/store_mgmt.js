import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    token: '',
    page: {},
    participant: {},
    printselection: [],
    routebeforelogin: '',
  },

  mutations: {
    updateToken (state, payload) {
      state.token = payload;
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