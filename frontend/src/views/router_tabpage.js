import Vue from 'vue'
import VueRouter from 'vue-router'
import TabPageView from '@/views/TabPageView.vue'

Vue.use(VueRouter);

const router = new VueRouter({
  routes: [
    {path: '/page/:slug/:lang', component: TabPageView},
    {path: '*', redirect: '/page/verblijfcatering/nl'},
  ],
  mode: 'history'
});

export default router