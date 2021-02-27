import Vue from 'vue'

const components = {
  Sidebar: () => import('../../components/Sidebar.vue' /* webpackChunkName: "components/sidebar" */).then(c => c.default || c)
}

for (const name in components) {
  Vue.component(name, components[name])
  Vue.component('Lazy' + name, components[name])
}
