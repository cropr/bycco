import Vue from 'vue'
import VueRouter from 'vue-router'
import PageAdd from '@/mgmt/PageAdd.vue'
import PageEdit from '@/mgmt/PageEdit.vue'
import PageList from '@/mgmt/PageList.vue'
import PagePreview from '@/mgmt/PagePreview.vue'

Vue.use(VueRouter);

const router = new VueRouter({
  routes: [
    {path: '/mgmt/page/list', component: PageList},
    {path: '/mgmt/page/add', component: PageAdd},
    {path: '/mgmt/page/edit/:id', component: PageEdit},
    {path: '/mgmt/page/preview:id', component: PagePreview},
    {path: '*', redirect: '/mgmt/page/list'},
  ],
  mode: 'history'
});

export default router