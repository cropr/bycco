'use strict';

angular.module('api')

.value('apischema',
   {
    base_url : '/api',
    schema: {
      // per api call define the required parameters per type
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
      uploadPhoto: {
        method: 'POST',
        url: '/subscriptions/{idsub}/photo',
        body: ['photo'],
        path: ['idsub'],
        required: ['photo', 'idsub']
      },


    }
  }
)

;
