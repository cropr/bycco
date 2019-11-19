import Vue from 'vue'
import VueRouter from 'vue-router'
import LandingView from '@/views/LandingView.vue'

Vue.use(VueRouter);

const router = new VueRouter({
  routes: [
    {path: '/page/:slug/:lang', component: LandingView},
    {path: '*', redirect: '/page/home/nl'},
  ],
  mode: 'history'
});

export default router