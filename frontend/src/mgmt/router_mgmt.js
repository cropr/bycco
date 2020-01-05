import Vue from 'vue'
import VueRouter from 'vue-router'
import PageAdd from '@/mgmt/PageAdd.vue'
import PageEdit from '@/mgmt/PageEdit.vue'
import PageList from '@/mgmt/PageList.vue'
import PagePreview from '@/mgmt/PagePreview.vue'
import ParticipantAdd from '@/mgmt/ParticipantAdd.vue'
import ParticipantBadge from '@/mgmt/ParticipantBadge.vue'
import ParticipantEdit from '@/mgmt/ParticipantEdit.vue'
import ParticipantList from '@/mgmt/ParticipantList.vue'
import ParticipantNamecard from '@/mgmt/ParticipantNamecard.vue'
import ParticipantPhoto from '@/mgmt/ParticipantPhoto.vue'
import ParticipantPresence from '@/mgmt/ParticipantPresence.vue'
import Login from '@/mgmt/Login.vue'


Vue.use(VueRouter);

const router = new VueRouter({
  routes: [
    {path: '/mgmt/page/list', component: PageList},
    {path: '/mgmt/page/add', component: PageAdd},
    {path: '/mgmt/page/edit/:id', component: PageEdit},
    {path: '/mgmt/page/preview/:id', component: PagePreview},
    {path: '/mgmt/participant/add', component: ParticipantAdd},
    {path: '/mgmt/participant/badge', component: ParticipantBadge},
    {path: '/mgmt/participant/edit/:id', component: ParticipantEdit},
    {path: '/mgmt/participant/list', component: ParticipantList},
    {path: '/mgmt/participant/namecard', component: ParticipantNamecard},
    {path: '/mgmt/participant/photo:/id', component: ParticipantPhoto},
    {path: '/mgmt/participant/presence', component: ParticipantPresence},
    {path: '/mgmt/login', component: Login},
    {path: '*', redirect: '/mgmt/page/list'},
  ],
  mode: 'history'
});

export default router