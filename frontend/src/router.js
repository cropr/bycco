
import Vue from 'vue'
import VueRouter from 'vue-router'

import Cms from '@/views/cms/Cms'
import NotFound from '@/views/NotFound'
import Subscription from '@/views/subscription/Subscription'
import Participants from '@/views/Participants'

Vue.use(VueRouter);

const router = new VueRouter({
  routes: [
    {path: '/page/:slug/:locale', component: Cms},
    {path: '/app/subscription/:locale', component: Subscription},
    {path: '/app/participant/:locale', component: Participants},
    {path: '*', component: NotFound},
  ],
  mode: 'history'
});

export default router;