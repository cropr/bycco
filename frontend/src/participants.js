'use strict';

angular.module('participants', [
  'ngAnimate',
  'ngAria',
  'ngMaterial',
  'ngSanitize'
])

.config(function($httpProvider){
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
})

.controller('partCtrl', function($scope, $http, $q, $log){

  var part_service = {
    getBoys: function(cat) {
      $scope.boys = [];
      var q = $q.defer();
      $http.get('/cd_subscription/api/participants/' + cat.boys).then(
        function(ro){
          $scope.boys = ro.data;
        },
        function(ro){
          console.error('getBoys', ro);
        }
      );
      return q.promise;
    },
    getGirls: function(cat) {
      $scope.girls = [];
      var q = $q.defer();
      $http.get('/cd_subscription/api/participants/' + cat.girls).then(
        function(ro){
          $scope.girls = ro.data;
        },
        function(ro){
          console.error('getGirls', ro);
        }
      );
      return q.promise;
    }
  };

  $scope.categories = [
    {label: '-8', boys:'B8', girls: 'G8'},
    {label: '-10', boys:'B10', girls: 'G10'},
    {label: '-12', boys:'B12', girls: 'G12'},
    {label: '-14', boys:'B14', girls: 'G14'},
    {label: '-16', boys:'B16', girls: 'G16'},
    {label: '-18', boys:'B18', girls: 'G18'},
    {label: '-20', boys:'B20', girls: 'G20'}
  ];

  $scope.loadcat = function(cat) {
    console.log('selected cat', cat);
    part_service.getBoys(cat);
    part_service.getGirls(cat);
  };

  $scope.photourl = function(p) {
    return '/cd_subscription/api/subscription/' + p.id + '/photo';
  };

  $scope.girls = [];

  $scope.boys = [];

});
