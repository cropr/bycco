export { default as Sidebar } from '../../components/Sidebar.vue'

export const LazySidebar = import('../../components/Sidebar.vue' /* webpackChunkName: "components/sidebar" */).then(c => c.default || c)
