export default {
  // per api call define the required parameters per type

  //attendee
  getAttendees: {
    method: 'GET',
    url: '/attendee',
    query: ['ss', 'cat', 'format'],
    required: [],
  },
  addAttendee: {
    method: 'POST',
    url: '/attendee',
    body: ['attendee'],
    required: ['attendee'],
  },
  getAttendee: {
    method: 'GET',
    url: '/attendee/{id}',
    path: ['id'],
    required: ['id'],
  },
  deleteAttendee: {
    method: 'DELETE',
    url: '/attendee/{id}',
    path: ['id'],
    required: ['id'],
  },
  updateAttendee: {
    method: 'PUT',
    url: '/attendee/{id}',
    path: ['id'],
    body: ['attendee'],
    required: ['attendee', 'id'],
  },
  resendConfirmation: {
    method: 'POST',
    url: '/attendee/{id}/resend',
    path: ['id'],
    required: ['id'],
  },

  // chess members
  searchIdNational: {
    method: 'GET',
    url: '/belplayer/{idbel}',
    path: ['idbel'],
    required: ['idbel'],
  },
  searchIdFide: {
    method: 'GET',
    url: '/fideplayer/{idfide}',
    path: ['idfide'],
    required: ['idfide'],
  },

  // subscription : to be checked if all methods are still used
  confirmSubscription: {
    method: 'POST',
    path: ['idsub'],
    url: '/subscriptions/{idsub}/confirm',
    required: ['idsub']
  },
  createSubscription: {
    method: 'POST',
    url: '/subscriptions',
    body: ['subscription'],
    required: ['subscription']
  },
  getPhoto: {
    method: 'GET',
    url: '/subscriptions/{idsub}/photo',
    path: ['idsub'],
    required: ['idsub']
  },
  getSubscription: {
    method: 'GET',
    url: '/subscriptions/{id}',
    path: ['id'],
    query: ['idtype'],
    required: ['id']
  },
  updateSubscription: {
    method: 'PUT',
    url: '/subscriptions',
    body: ['subscription'],
    required: ['subscription']
  },
  uploadPhoto: {
    method: 'POST',
    url: '/subscriptions/{idsub}/photo',
    body: ['photo'],
    path: ['idsub'],
    required: ['photo', 'idsub']
  },

  //tournamanet
  addTournament: {
    method: 'POST',
    url: '/tournament',
    body: ['name', 'shortname', 'rounds'],
    required: ['name', 'shortname', 'rounds'],
  },
  getTournaments: {
    method: 'GET',
    url: '/tournament',
    required: [],
  },
  getPairings: {
    method: 'GET',
    url: '/tournament/{id_trn}/pairings/{round}',
    path: ['id_trn', 'round'],
    required: ['id_trn', 'round'],
  },
  getParticipants: {
    method: 'GET',
    url: '/participants',
  },
  getStandings: {
    method: 'GET',
    url: '/tournament/{id_trn}/standings/{round}',
    path: ['id_trn', 'round'],
    required: ['id_trn', 'round'],
  },
  getTopround: {
    method: 'GET',
    url: '/tournament/{id_trn}/topround',
    path: ['id_trn'],
    required: ['id_trn'],
  },
  getPdfGames: {
    method: 'GET',
    url: '/tournament/{id_trn}/pdfgames',
    path: ['id_trn'],
    required: ['id_trn'],
  },
  getPgnGames: {
    method: 'GET',
    url: '/tournament/{id_trn}/pgngames',
    path: ['id_trn'],
    required: ['id_trn'],
  },
  getPrizes: {
    method: 'GET',
    url: '/tournament/{id_trn}/prizes',
    path: ['id_trn'],
    required: ['id_trn'],
  },
  createPrizes: {
    method: 'POST',
    url: '/tournament/{id_trn}/prizes',
    path: ['id_trn'],
    required: ['id_trn'],
  },

  // swar
  uploadSwarJson: { // use _body
    method: 'POST',
    url: '/swar',
    body: ['name', 'jsonfile', 'round', 'id_trn'],
    required: ['name', 'jsonfile', 'round', 'id_trn'],
  },
  getSwarTournaments: {
    method: 'GET',
    url: '/swar',
    required: [],
  },

  getSwarFiles: {
    method: 'GET',
    url: '/swar/{id_swartrn}/file',
    path: ['id_swartrn'],
    required: ['id_swartrn'],
  },
  getSwarFile: {
    method: 'GET',
    url: '/swar/{id_swartrn}/file/{id_swarfile}',
    path: ['id_swartrn', 'id_swarfile'],
    required: ['id_swartrn', 'id_swarfile'],
  },
  removeSwarFile: {
    method: 'DELETE',
    url: '/swar/{id_swartrn}/file/{id_swarfile}',
    path: ['id_swartrn', 'id_swarfile'],
    required: ['id_swartrn', 'id_swarfile'],
  },
  publishSwarFile: {
    method: 'POST',
    url: '/swar/{id_swartrn}/publication/{id_swarfile}',
    path: ['id_swartrn', 'id_swarfile'],
    required: ['id_swartrn', 'id_swarfile'],
  },

  //invoices
  createInvoice: {
    method: 'POST',
    url: '/invoice/{id_participant}',
    path: ['id_participant'],
    required: ['id_participant'],
  },
  getInvoice: {
    method: 'GET',
    url: '/invoice/{id_participant}',
    path: ['id_participant'],
    required: ['id_participant'],
  },
  sendInvoice: {
    method: 'POST',
    url: '/invoice/{id_participant}/send',
    path: ['id_participant'],
    required: ['id_participant'],
  },
  invoices: {
    method: 'POST',
    url: '/invoice',
    body: ['command', 'options'],
    required: ['command'],
  },
  getLanguageFile: {
    method: 'GET',
    url: '/lang/{lang}',
    path: ['lang'],
    required: ['lang']    
  },

  // page and slugs
  getPageBySlugLocale: {
    method: 'GET',
    url: '/slug/{slug}/locale/{locale}',
    path: ['slug', 'locale'],
    required: ['slug', 'locale'],
  },
  getPageBySlug: {
    method: 'GET',
    url: '/slug/{slug}',
    path: ['id'],
    required: ['id'],
  },
  getPageById: {
    method: 'GET',
    url: '/page/{id}',
    path: ['id'],
    required: ['id'],
  },
  updatePage: {
    method: 'PUT',
    url: '/page/{id}',
    path: ['id'],
    body: ['page'],
    required: ['id', 'page'],
  },
  getPages: {
    method: 'GET',
    url: '/page',
    headers: ['Authorization']
  },

  // account
  login: {
    method: 'POST',
    url: '/login',
    body: ['username', 'password', 'command'],
    required: ['command'],
  },

};
