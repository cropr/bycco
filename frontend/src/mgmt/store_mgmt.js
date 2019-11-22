import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    page: {},
  },

  mutations: {
    updatePage (state, payload) {
      state.page = payload;
    },
  }
})

export default store