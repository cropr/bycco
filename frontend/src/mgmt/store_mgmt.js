import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    account: {},
    page: {},
    routebeforelogin: '',
  },

  mutations: {
    updateAccount (state, payload) {
      state.account = payload;
    },
    updatePage (state, payload) {
      state.page = payload;
    },
    updateRouteBeforeLogin (state, payload) {
      state.routebeforelogin = payload;
    },
  }
})

export default store