import Vue from 'vue'
import Vuex from 'vuex'
// import _ from "lodash";

Vue.use(Vuex);

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
    authenticated: false,
    drawer: false,
    subscription: {},
    photo: '',
    flow: initflow,
  },
  mutations: {

    // drawer
    updateDrawer(state, value) {
      state.drawer = value;
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
      state.flow = initflow;
      state.subscription = {};
      state.photo = '';
    },
    updateFlow(state, payload){
      state.flow = Object.assign({}, state.flow, payload)
    },
  }
});

export default store


