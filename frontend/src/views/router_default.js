import Vue from 'vue'
import VueRouter from 'vue-router'
import DefaultView from '@/views/DefaultView.vue'

Vue.use(VueRouter);

const router = new VueRouter({
  routes: [
    {path: '/page/:slug/:lang', component: DefaultView},
    {path: '*', redirect: '/page/toernooireglement/nl'},
  ],
  mode: 'history'
});

export default router