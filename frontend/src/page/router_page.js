import Vue from 'vue'
import VueRouter from 'vue-router'

import RouteNotFound from './RouteNotFound.vue'

Vue.use(VueRouter);

const router = new VueRouter({
  routes: [
    {path: '*', component: RouteNotFound},
  ],
  mode: 'history'
});

//  dynamic adding of routes possible

import CmsSimplePage from './CmsSimplePage.vue'
import LandingPage from './LandingPage.vue'
import MultiLocalePage from './MultiLocalePage.vue'
import Subscription from '@/app-pages/Subscription.vue'
import Participants from '@/app-pages/Participants.vue'

let dynroutes = {
  CmsSimplePage: CmsSimplePage,
  LandingPage: LandingPage,
  MultiLocalePage: MultiLocalePage,
  Subscription: Subscription,
  Participants: Participants,
}


function processRoutes(rts) {
  // cycle through routes from api and construct routing table 
  let rtable = [];
  rts.forEach(function(rt) {
    rtable.push({
      component: (rt.component in dynroutes) ? dynroutes[rt.component] : RouteNotFound,
      path: '/page/' + rt.slug + '/:locale'
    })
  })
  return rtable
}


export {router, processRoutes};