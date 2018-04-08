export default {
  // per api call define the required parameters per type

  //attendee
  getAttendees: {
    method: 'GET',
    url: '/attendees',
    query: ['ss', 'start', 'count', 'cat'],
    required: [],
  },
  addAttendee: {
    method: 'POST',
    url: '/attendees',
    body: ['attendee'],
    required: ['attendee'],
  },
  getAttendee: {
    method: 'GET',
    url: '/attendees/{id}',
    path: ['id'],
    required: ['id'],
  },
  deleteAttendee: {
    method: 'DELETE',
    url: '/attendees/{id}',
    path: ['id'],
    required: ['id'],
  },
  updateAttendee: {
    method: 'PUT',
    url: '/attendees/{id}',
    path: ['id'],
    body: ['attendee'],
    required: ['attendee', 'id'],
  },
  resendConfirmation: {
    method: 'POST',
    url: '/attendees/{id}/resend',
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
  updateSubscription: {
    method: 'PUT',
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
};
