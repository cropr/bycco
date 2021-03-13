import Vue from 'vue'

const components = {
  AdCarousel: () => import('../../components/AdCarousel.vue' /* webpackChunkName: "components/ad-carousel" */).then(c => c.default || c),
  ByccoFooter: () => import('../../components/ByccoFooter.vue' /* webpackChunkName: "components/bycco-footer" */).then(c => c.default || c),
  Sidebar: () => import('../../components/Sidebar.vue' /* webpackChunkName: "components/sidebar" */).then(c => c.default || c),
  Topbar: () => import('../../components/Topbar.vue' /* webpackChunkName: "components/topbar" */).then(c => c.default || c)
}

for (const name in components) {
  Vue.component(name, components[name])
  Vue.component('Lazy' + name, components[name])
}
