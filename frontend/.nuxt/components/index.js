export { default as AdCarousel } from '../../components/AdCarousel.vue'
export { default as ByccoFooter } from '../../components/ByccoFooter.vue'
export { default as Sidebar } from '../../components/Sidebar.vue'
export { default as Topbar } from '../../components/Topbar.vue'

export const LazyAdCarousel = import('../../components/AdCarousel.vue' /* webpackChunkName: "components/ad-carousel" */).then(c => c.default || c)
export const LazyByccoFooter = import('../../components/ByccoFooter.vue' /* webpackChunkName: "components/bycco-footer" */).then(c => c.default || c)
export const LazySidebar = import('../../components/Sidebar.vue' /* webpackChunkName: "components/sidebar" */).then(c => c.default || c)
export const LazyTopbar = import('../../components/Topbar.vue' /* webpackChunkName: "components/topbar" */).then(c => c.default || c)
