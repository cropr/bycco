import Vue from 'vue'
import VueRouter from 'vue-router'
import DefaultView from '@/user/DefaultView.vue'
import LandingView from '@/user/LandingView.vue'
import AgendaView from '@/user/AgendaView.vue'
import DocDefault from '@/user/DocDefault.vue'
import DocLanding from '@/user/DocLanding.vue'
import DocAgenda from '@/user/DocAgenda.vue'

Vue.use(VueRouter);

const router = new VueRouter({
  routes: [
    {path: '/page/home/:lang', component: LandingView},
    {path: '/page/huisreglement/:lang', component: DefaultView},
    {path: '/page/restaurant/:lang', component: DefaultView},
    {path: '/page/toernooireglement/:lang', component: DefaultView},
    {path: '/page/toewijzingverblijf/:lang', component: DefaultView},
    {path: '/page/verblijf/:lang', component: DefaultView},
    {path: '/page/agenda/:lang', component: AgendaView},
    {path: '/doc/home/:lang', component: DocLanding},
    {path: '/doc/huisreglement/:lang', component: DocDefault},
    {path: '/doc/restaurant/:lang', component: DocDefault},
    {path: '/doc/toernooireglement/:lang', component: DocDefault},
    {path: '/doc/toewijzingverblijf/:lang', component: DocDefault},
    {path: '/doc/verblijf/:lang', component: DocDefault},
    {path: '/doc/agenda/:lang', component: DocAgenda},    
  ],
  mode: 'history'
});

export default router