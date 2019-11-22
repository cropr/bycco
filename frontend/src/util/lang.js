import Vue from 'vue'
import VueI18n from 'vue-i18n'
import api from '../util/api';

Vue.use(VueI18n);

let messages = { en: {}}, warninggiven = false;

const loadedLanguages = []

function missingHandler(locale, key){
  let shortkey = key.substring(0,20)
  if (loadedLanguages.includes(locale)) {
    console.warn('Missing translation for key: "' + shortkey + '" in locale ' + locale)
  }
  else if (!warninggiven) {
    console.warn('locale ' + locale + ' not yet loaded')
    warninggiven = true;
  }
}

export const i18n = new VueI18n({
  locale: 'en', 
  fallbackLocale: 'en',
  messages,
  silentTranslationWarn: true,
  silentFallbackWarn: true,
})

export function setLanguage(lang) {
  if (i18n.locale === lang  && loadedLanguages.includes(lang) ) {
    return Promise.resolve(function(lang){
      i18n.locale = lang;
    })
  }
  loadLanguage(lang);
}

export function loadLanguage(lang) {
  api('getLanguageFile', {
    lang: lang
  }).then( 
    function(data){
      i18n.setLocaleMessage(lang, data);
      loadedLanguages.push(lang);
      i18n.locale = lang;
      i18n.missing = missingHandler;
      i18n.silentTranslationWarn = false;
    },
    function( data) {
      console.error('failed getting language file', data)
    }
  );
} 