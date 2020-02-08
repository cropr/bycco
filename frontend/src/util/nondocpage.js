
let store = null;

export function changeLocale(l) {
  if (l == store.state.locale) return;
  store.commit('updateLocale', l);
}

export function start(vm) {
  store = vm.$store;
  changeLocale();
}

export function changeSlug() {}

export function getPageContent() {}

export function getDocContent() {}
