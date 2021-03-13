import Vue from 'vue'
import Router from 'vue-router'
import { normalizeURL, decode } from 'ufo'
import { interopDefault } from './utils'
import scrollBehavior from './router.scrollBehavior.js'

const _41e2770f = () => interopDefault(import('../pages/index.vue' /* webpackChunkName: "pages/index" */))
const _277ed345 = () => interopDefault(import('../pages/toernooireglement.vue' /* webpackChunkName: "pages/toernooireglement" */))

const emptyFn = () => {}

Vue.use(Router)

export const routerOptions = {
  mode: 'history',
  base: '/',
  linkActiveClass: 'nuxt-link-active',
  linkExactActiveClass: 'nuxt-link-exact-active',
  scrollBehavior,

  routes: [{
    path: "/de",
    component: _41e2770f,
    name: "index___de"
  }, {
    path: "/en",
    component: _41e2770f,
    name: "index___en"
  }, {
    path: "/fr",
    component: _41e2770f,
    name: "index___fr"
  }, {
    path: "/nl",
    component: _41e2770f,
    name: "index___nl"
  }, {
    path: "/toernooireglement",
    component: _277ed345,
    name: "toernooireglement"
  }, {
    path: "/de/toernooireglement",
    component: _277ed345,
    name: "toernooireglement___de"
  }, {
    path: "/en/toernooireglement",
    component: _277ed345,
    name: "toernooireglement___en"
  }, {
    path: "/fr/toernooireglement",
    component: _277ed345,
    name: "toernooireglement___fr"
  }, {
    path: "/nl/toernooireglement",
    component: _277ed345,
    name: "toernooireglement___nl"
  }, {
    path: "/",
    component: _41e2770f,
    name: "index"
  }],

  fallback: false
}

export function createRouter (ssrContext, config) {
  const base = (config.app && config.app.basePath) || routerOptions.base
  const router = new Router({ ...routerOptions, base  })

  // TODO: remove in Nuxt 3
  const originalPush = router.push
  router.push = function push (location, onComplete = emptyFn, onAbort) {
    return originalPush.call(this, location, onComplete, onAbort)
  }

  const resolve = router.resolve.bind(router)
  router.resolve = (to, current, append) => {
    if (typeof to === 'string') {
      to = normalizeURL(to)
    }
    return resolve(to, current, append)
  }

  return router
}
