import * as moment from 'moment'
import 'moment/locale/nl'
import 'moment/locale/fr'
import 'moment/locale/de'

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


export {formatDate, navigation, setNavigation};