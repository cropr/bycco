import Vue from 'vue'
import VueRouter from 'vue-router'
import PagesView from '@/mgmt/Pages.vue'

Vue.use(VueRouter);

const router = new VueRouter({
  routes: [
    {path: '/pages', component: PagesView},
    {path: '*', redirect: '/pages'},
  ],
  mode: 'history'
});

export default router