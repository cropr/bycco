import Vue from 'vue'
import VueRouter from 'vue-router'
import BMemberAdd from '@/mgmt/BMemberAdd.vue'
import BMemberEdit from '@/mgmt/BMemberEdit.vue'
import BMemberList from '@/mgmt/BMemberList.vue'
import BRoleAdd from '@/mgmt/BRoleAdd.vue'
import BRoleEdit from '@/mgmt/BRoleEdit.vue'
import BRoleList from '@/mgmt/BRoleList.vue'
import FileAdd from '@/mgmt/FileAdd.vue'
import FileEdit from '@/mgmt/FileEdit.vue'
import FileList from '@/mgmt/FileList.vue'
import PageAdd from '@/mgmt/PageAdd.vue'
import PageEdit from '@/mgmt/PageEdit.vue'
import PageList from '@/mgmt/PageList.vue'
import Login from '@/mgmt/Login.vue'


Vue.use(VueRouter);

const router = new VueRouter({
  routes: [
    {path: '/mgmt/brole/list', component: BRoleList},
    {path: '/mgmt/brole/add', component: BRoleAdd},
    {path: '/mgmt/brole/edit/:id', component: BRoleEdit},
    {path: '/mgmt/bmember/list', component: BMemberList},
    {path: '/mgmt/bmember/add', component: BMemberAdd},
    {path: '/mgmt/bmember/edit/:id', component: BMemberEdit},
    {path: '/mgmt/file/add', component: FileAdd},
    {path: '/mgmt/file/edit/:id', component: FileEdit},
    {path: '/mgmt/file/list', component: FileList},
    {path: '/mgmt/page/list', component: PageList},
    {path: '/mgmt/page/add', component: PageAdd},
    {path: '/mgmt/page/edit/:id', component: PageEdit},
    {path: '/mgmt/login', component: Login},
    {path: '*', redirect: '/mgmt/page/list'},
  ],
  mode: 'history'
});

export default router