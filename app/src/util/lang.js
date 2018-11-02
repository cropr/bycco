import Vue from 'vue'
import VueI18n from 'vue-i18n'
import en from './en'
import axios from 'axios'

Vue.use(VueI18n);

export const i18n = new VueI18n({
  locale: 'en', // set locale
  fallbackLocale: 'en',
  messages: { en } // set locale messages
})

const loadedLanguages = [ ' en'] // our default language that is preloaded

function setI18nLanguage (lang) {
  console.log('setting language to ', lang)
  i18n.locale = lang;
  axios.defaults.headers.common['Accept-Language'] = lang
  document.querySelector('html').setAttribute('lang', lang)
  return lang
}

export function loadLanguageAsync (lang) {
  console.log('loading lang', lang);
  if (i18n.locale !== lang) {
    if (!loadedLanguages.includes(lang)) {
      axios.get('/static/lang/' + lang + '.json').then(data => {
        console.log('loaded lang', data.data)
        i18n.setLocaleMessage(lang, data.data)
        loadedLanguages.push(lang)
        return setI18nLanguage(lang)
      })
    }
    return Promise.resolve(setI18nLanguage(lang))
  }
  return Promise.resolve(lang)
}
