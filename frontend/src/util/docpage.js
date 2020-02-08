import api from '@/util/api'

let store = null;
let router = null;

export function start(vm) {
  store = vm.$store;
  router = vm.$router;
  changeSlug(window.config.slug)
  console.log('check 302');
}

export function getDocContent () {
 if (!store.state.slug) return;
  api('getDoc', {
    idtype: 'slug',
    id: store.state.slug,
    locale: store.state.locale,
  }).then(function(data){
    store.commit('updateDoc', data.document)
  }, function(data) {
    console.error('error loading document', data);
  })
}

export function changeSlug(s) {
  console.log('changing slug:', s)
  if (s == store.state.slug) return;
  store.commit('updateDocUrl', {slug:s});
  router.push('/doc/' + store.state.slug + '/' + store.state.locale)
}

export function changeLocale(l) {
  console.log('changing locale', l)
  if (l == store.state.locale) return;
  store.commit('updateDocUrl', {locale:l});
  router.push('/doc/' + store.state.slug + '/' + store.state.locale)    
}
