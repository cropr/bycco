import api from '@/util/api'

let store = null;
let router = null;

export function startPage(vm) {
  store = vm.$store;
  router = vm.$router;
  changeSlug(window.config.slug)
}

export function getPageContent () {
 if (!store.state.slug) return;
  api('getPageBySlugLocale', {
    slug: store.state.slug,
    locale: store.state.locale,
  }).then(function(data){
    store.commit('updatePage', data.page)
  }, function(data) {
    console.error('error loading page', data);
  })
}

export function changeSlug(s) {
  console.log('changing slug', s)
  if (s == store.state.slug) return;
  store.commit('updatePageUrl', {slug:s});
  router.push('/page/' + store.state.slug + '/' + store.state.locale)      
}

export function changeLocale(l) {
  if (l == store.state.locale) return;
  store.commit('updatePageUrl', {locale:l});
  router.push('/page/' + store.state.slug + '/' + store.state.locale)    
}
