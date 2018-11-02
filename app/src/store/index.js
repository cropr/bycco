import Vue from 'vue'
import Vuex from 'vuex'
// import _ from "lodash";

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    authenticated: false,
    drawer: false,
  },
  mutations: {
    updateDrawer(state, value) {
      state.drawer = value;
    }
  },
});

export default store
