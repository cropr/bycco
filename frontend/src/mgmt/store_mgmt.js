import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    token: '',
    page: {},
    routebeforelogin: '',
  },

  mutations: {
    updateToken (state, payload) {
      console.log('storing token', payload)
      state.token = payload;
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