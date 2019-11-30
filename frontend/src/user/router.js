import Vue from 'vue'
import VueRouter from 'vue-router'
import DefaultView from '@/user/DefaultView.vue'
import LandingView from '@/user/LandingView.vue'

Vue.use(VueRouter);

const router = new VueRouter({
  routes: [
    {path: '/page/home/:lang', component: LandingView},
    {path: '/page/huisreglement/:lang', component: DefaultView},
    {path: '/page/restaurant/:lang', component: DefaultView},
    {path: '/page/toernooireglement/:lang', component: DefaultView},
    {path: '/page/toewijzingverblijf/:lang', component: DefaultView},
    {path: '/page/verblijf/:lang', component: DefaultView},
  ],
  mode: 'history'
});

export default router