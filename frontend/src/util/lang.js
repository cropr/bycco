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

const loadedLanguages = [ 'en'] // our default language that is preloaded

function setI18nLanguage (lang) {
  console.log('set language', lang)
  i18n.locale = lang;
  axios.defaults.headers.common['Accept-Language'] = lang
  document.querySelector('html').setAttribute('lang', lang)
}

export function loadLanguageAsync (lang) {
  if (i18n.locale !== lang) {
    if (!loadedLanguages.includes(lang)) {
      console.log('loading language', lang)
      axios.get('/static/lang/' + lang + '.json').then(data => {
        i18n.setLocaleMessage(lang, data.data)
        loadedLanguages.push(lang)
        setI18nLanguage(lang);
        return
      })
    }
    else {
      setI18nLanguage(lang)
    }
  }
}
