import * as moment from 'moment'
import 'moment/locale/nl'
import 'moment/locale/fr'
import 'moment/locale/de'

const categories = [
  {value: 20, text: '-20', year: 2000},
  {value: 18, text: '-18', year: 2002},
  {value: 16, text: '-16', year: 2004},
  {value: 14, text: '-14', year: 2006},
  {value: 12, text: '-12', year: 2008},
  {value: 10, text: '-10', year: 2010},
  {value: 8, text: '-8', year: 2012},
];

function formatDate(d){
  return d ? moment(d).format('DD MMMM YYYY'): ''
}

let navigation = {
  getPageContent: function(){},
  changeSlug: function(){},
  changeLocale: function(){},
}

function setNavigation(n,f) {
  navigation[n] = f
}

export {categories, formatDate, navigation, setNavigation};