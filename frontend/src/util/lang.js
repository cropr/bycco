import Vue from 'vue'
import VueI18n from 'vue-i18n'
import en from './en'
import nl from './nl'
import fr from './fr'
import de from './de'


Vue.use(VueI18n);

let messages = { 
  en: en,
  fr: fr,
  nl: nl,
  de: de,
}

export const i18n = new VueI18n({
  locale: 'en', 
  fallbackLocale: 'en',
  messages, 
  // silentTranslationWarn: true  
})

export const locales = ['nl', 'fr', 'de', 'en']

export function setLanguage(lang) {
  i18n.locale = lang;
}

