import * as moment from 'moment'
import 'moment/locale/nl'
import 'moment/locale/fr'
import 'moment/locale/de'

const categories = [
  {value: 20, text: '-20', year: 1999},
  {value: 18, text: '-18', year: 2001},
  {value: 16, text: '-16', year: 2003},
  {value: 14, text: '-14', year: 2005},
  {value: 12, text: '-12', year: 2007},
  {value: 10, text: '-10', year: 2009},
  {value: 8, text: '-8', year: 2011}
];

function formatDate(d){
  return d ? moment(d).format('DD MMMM YYYY'): ''
}

export {categories, formatDate};