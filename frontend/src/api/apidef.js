export default {
  // per api call define the required parameters per type
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
  }
};
