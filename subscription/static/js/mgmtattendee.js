// original Copyright Ruben Decrop 2012
// modifications by Chessdevil Consulting BVBA 2016-2017

'use strict';

angular.module('mgmtattendee', [
  'ngAnimate',
  'ngAria',
  'ngFileUpload',
  'ngImgCrop',
  'ngMaterial',
  'ngSanitize'
])

.config(function($httpProvider){
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
})

.controller('mgmtAttendeeCtrl', function($scope, $http, $q, $log){

  var randomstr = '12345';

  var mgmtattendee_service = {
    addAttendee: function() {
      var q = $q.defer();
      $http.post('/cd_subscription/api/attendee', $scope.attendee).then(
        function(ro){
          $log.info('Attendee added', ro.data);
          q.resolve(ro.data);

        },
        function(ro){
          $log.error('getAttendees', ro);
          q.reject(ro);
        }
      );
      return q.promise;
    },
    deleteAttendee: function() {
      var q = $q.defer();
      $http.delete('/cd_subscription/api/attendee/' + $scope.attendee.id_national).then(
        function(ro){
          $log.info('Attendee deleted');
          q.resolve();
        },
        function(ro){
          $log.error('getAttendees', ro);
          q.reject(ro);
        }
      );
      return q.promise;
    },
    getAttendees: function() {
      $scope.players = [];
      var q = $q.defer();
      $http.get('/cd_subscription/api/attendee', {params:queryParams()}).then(
        function(ro){
          $log.info('gotPlayers', ro.data);
          $scope.players = ro.data.attendees;
          $scope.att.ss = ro.data.ss || "";
          $scope.att.cat = ro.data.cat || "";
          updatePager(ro.data.start, ro.data.count, ro.data.n_attendees)
        },
        function(ro){
          $log.error('getAttendees', ro);
        }
      );
      return q.promise;
    },
    getAttendee: function(id){
      var q = $q.defer();
      $http.get('/cd_subscription/api/attendee/' + id).then(
        function(ro){
          $log.info('gotAttendee', ro.data);
          $scope.attendee = ro.data.attendee;
        },
        function(ro){
          $log.error('getAttendee', ro);
        }
      );
      return q.promise;
    },
    printallbadges: function(){
      window.open('/cd_subscription/printallbadges', "_print")
    },
    printbadges: function(ids) {
      var qstr = ids.join('&');
      window.open('/cd_subscription/printbadges?' + qstr, "_print");
    },
    printallnamecards: function(){
      window.open('/cd_subscription/printallnamecards', "_print")
    },
    printnamecards: function(ids) {
      var qstr = ids.join('&');
      window.open('/cd_subscription/printnamecards?' + qstr, "_print");
    },
    updateAttendee: function() {
      var q = $q.defer();
      $http.put('/cd_subscription/api/attendee/' + $scope.attendee.id_national,
          $scope.attendee).then(
        function(ro){
          $log.info('Attendee updated');
          q.resolve(ro.data);
        },
        function(ro){
          $log.error('getAttendees', ro);
          q.reject(ro);
        }
      );
      return q.promise;
    },
    uploadPhoto: function(id, imagedata){
      var q = $q.defer();
      $http.post('/cd_subscription/api/attendee/' + id + '/photo',
            {imagedata: imagedata}).then(
        function(ro){
          $log.info('photo uploeded');
          initPhoto($scope.attendee);
        },
        function(ro){
          $log.error('uploadPhoto', ro);
        }
      );
      return q.promise;
    }
  };

  function queryParams(){
    return {
      start: $scope.pager.start,
      count: $scope.pager.count,
      ss: $scope.att.ss.length ? $scope.att.ss : null,
      cat: $scope.att.cat ? $scope.att.cat : null
    }
  }

  function updatePager(start, count, total) {
    angular.extend($scope.pager, {
      start: start,
      count: count,
      total: total,
      end: Math.min(start+count, total),
      show: total>count,
      active: -1,
      pages: []
    });
    for (var i=0; i<total; i+=count) {
      var page = {};
      if (i>= start && i < start + count) {
        $scope.pager.active = i;
        page.active = true;
      }
      $scope.pager.pages.push(page);
    }
  }

  $scope.pager = {
    count: 25,
    start: 0,
    goto: function(i) {
      $scope.pager.start = i * $scope.pager.count;
      mgmtattendee_service.getAttendees();
    },
    next: function(){
      if ($scope.pager.start + $scope.pager.count < $scope.pager.total) {
        $scope.pager.start += $scope.pager.count;
        mgmtattendee_service.getAttendees();
      }
    },
    prev: function(){
      if ($scope.pager.start > 0) {
        $scope.pager.start -= $scope.pager.count;
        if ($scope.pager.start < 0) $scope.pager.start = 0;
        mgmtattendee_service.getAttendees();
      }
    }
  };

  $scope.photourl = function(p){
    return '/cd_subscription/api/attendee/' + ((p && p.id_national) ?
            p.id_national:0) + '/photo?' + randomstr  ;
  };

  $scope.att = {
    ss:'',
    status: '',
    add_badge: function(p){
      $scope.badges.push(p);
    },
    add_card: function(p){
      $scope.cards.push(p);
    },
    ask_delete: function(){
      if (confirm("Are you sure to delete " + $scope.attendee.name + " " +
          $scope.attendee.firstname + "?")) {
        mgmtattendee_service.deleteAttendee().then(initAttendees);
      }
    },
    cancel: function(){
      this.status = '';
    },
    open_add: function(){
      this.status = 'add';
      angular.extend($scope.attendee,{
        name: '',
        firstname: '',
        chesstitle: '',
        category: 'EAT',
        gender: 'M',
        meals: ''
      });
    },
    open_edit: function(p){
      this.status = 'edit';
      mgmtattendee_service.getAttendee(p.id_national);
    },
    open_photo: function(p){
      initPhoto(p);
    },
    save_add: function(){
      mgmtattendee_service.addAttendee().then(
        function(data){
          alert('Attendee saved with id: ' + data.id_national);
          $scope.att.status = 'addsaved';
          $scope.attendee.id_national = data.id_national;
        },
        function(ro) {
          alert(ro);
        }
      )
    },
    save_edit: function(){
      mgmtattendee_service.updateAttendee().then(
        function(data){
          alert('Attendee ' + data.id_national + ' updated');
          $scope.att.status = 'editsaved';
          $log.info('cat', $scope.att.cat);
          mgmtattendee_service.getAttendees();
        },
        function(ro) {
          alert(ro);
        }
      )    },
    search: function(){
        mgmtattendee_service.getAttendees();
    },
    show_add: function(){
      return this.status == 'add' || this.status == 'addsaved';
    },
    show_edit: function(){
      return this.status == 'edit' || this.status == 'editsaved';
    }
  };

  $scope.badges = [];

  $scope.bdg = {
    clearselected: function(){
      $scope.badges = [];
    },
    printall: mgmtattendee_service.printallbadges,
    printselected: function(){
      var ids = [];
      $scope.badges.forEach(function(v,ix) {
        ids.push(v.id_national);
      });
      mgmtattendee_service.printbadges(ids);
    },
    remove_single: function(p){
      var dix = -1;
      $scope.badges.forEach(function(v,ix){
        if (v.id_national == p.id_national) dix = ix;
      });
      if (dix>=0) {
        $scope.badges.splice(dix, 1);
      }
    }
  };

  $scope.cards = [];

  $scope.crd = {
    clearselected: function(){
      $scope.cards = [];
    },
    printall: mgmtattendee_service.printallnamecards,
    printselected: function(){
      var ids = [];
      $scope.cards.forEach(function(v,ix) {
        ids.push(v.id_national);
      });
      mgmtattendee_service.printnamecards(ids);
    },
    remove_single: function(p){
      var dix = -1;
      $scope.cards.forEach(function(v,ix){
        if (v.id_national == p.id_national) dix = ix;
      });
      if (dix>=0) {
        $scope.cards.splice(dix, 1);
      }
    }
  };

  $scope.photo = {
    data: "",
    init: function(){
      angular.extend($scope.photo, {
        data: "",
        cropsource: "",
        cropresult: "?1234"
      });
    },
    upload: function(){
      if (!$scope.photo.cropresult || !$scope.photo.cropresult.length) return;
      mgmtattendee_service.uploadPhoto($scope.attendee.id_national,
          $scope.photo.cropresult);

    }
  };

  $scope.$watch('photo.data', function () {
    var reader;
    $scope.filename = $scope.photo.data.name + '';
    if ($scope.photo.data.name) {
      reader = new FileReader();
      reader.onload = function (evt) {
        $scope.$apply(function($scope){
          $scope.photo.cropsource = evt.target.result;
        });
      };
      reader.readAsDataURL($scope.photo.data);
    }
  });

  function initAttendees(){
    $scope.players = [];
    $scope.attendee = {};
    $scope.att.ss = "";
    $scope.tab = 0;
    $scope.att.status = '';
    mgmtattendee_service.getAttendees();
  }

  function initPhoto(p){
    $scope.attendee = {};
    $scope.tab = 1;
    randomstr = Math.ceil(Math.random()*10000);
    mgmtattendee_service.getAttendee(p.id_national);
    $scope.photo.init()
  }



  initAttendees();

});
