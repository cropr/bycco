import Vue from 'vue'
import VueRouter from 'vue-router'
import EnrollmentAdd from '@/mgmt/EnrollmentAdd'
import EnrollmentEdit from '@/mgmt/EnrollmentEdit'
import EnrollmentList from '@/mgmt/EnrollmentList'
// import FileAdd from '@/mgmt/FileAdd.vue'
// import FileEdit from '@/mgmt/FileEdit.vue'
// import FileList from '@/mgmt/FileList.vue'
import PageAdd from '@/mgmt/PageAdd.vue'
import PageEdit from '@/mgmt/PageEdit.vue'
import PageList from '@/mgmt/PageList.vue'
import Login from '@/mgmt/Login.vue'
import SwarTrnAdd from '@/mgmt/SwarTrnAdd.vue'
import SwarTrnEdit from '@/mgmt/SwarTrnEdit.vue'
import SwarTrnList from '@/mgmt/SwarTrnList.vue'



Vue.use(VueRouter);

const router = new VueRouter({
  routes: [
    {path: '/mgmt/enrollment/list', component: EnrollmentList},
    {path: '/mgmt/enrollment/add', component: EnrollmentAdd},
    {path: '/mgmt/enrollment/edit/:id', component: EnrollmentEdit},
    // {path: '/mgmt/file/add', component: FileAdd},
    // {path: '/mgmt/file/edit/:id', component: FileEdit},
    // {path: '/mgmt/file/list', component: FileList},
    {path: '/mgmt/page/list', component: PageList},
    {path: '/mgmt/page/add', component: PageAdd},
    {path: '/mgmt/page/edit/:id', component: PageEdit},
    {path: '/mgmt/login', component: Login},
    {path: '/mgmt/swartrn/add', component: SwarTrnAdd},
    {path: '/mgmt/swartrn/edit/:id', component: SwarTrnEdit},
    {path: '/mgmt/swartrn/list', component: SwarTrnList},
    {path: '*', redirect: '/mgmt/page/list'},
  ],
  mode: 'history'
});

export default router