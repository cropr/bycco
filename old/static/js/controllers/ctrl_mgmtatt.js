
angular.module('mg_attendee', [
  'ngAnimate',
  'ngAria',
  'ngFileUpload',
  'ngMaterial',
  'ngSanitize',
  'uiCropper',
  'common'
])

.controller('mgAttendeeCtrl', function($scope, $http, $q, $log, $timeout, api){

  var randomstr = '12345',
      tabs = {
        overview: 0,
        detail: 1,
        photo: 2,
        print: 3
      };

  var attendee_service = {
    addAttendee: function() {
      var q = $q.defer();
      api('addAttendee', {attendee:$scope.attendee}).then(
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
      api('deleteAttendee', {idattendee: $scope.attendee.id_national}).then(
        function(ro){
          $log.info('Attendee deleted');
          $timeout(q.resolve);
        },
        function(ro){
          $log.error('getAttendees', ro);
          $timeout(function(){q.reject(ro)});
        }
      );
      return q.promise;
    },
    getAttendees: function() {
      $scope.players = [];
      var q = $q.defer();
      api('getAttendees', {
        start: $scope.pager.start,
        count: $scope.pager.count,
        ss: $scope.att.ss.length ? $scope.att.ss : null,
        cat: $scope.att.cat ? $scope.att.cat : null
      }).then(
        function(data){
          $log.info('gotPlayers', data);
          $timeout(function() {
            $scope.players = data.attendees;
            $scope.att.ss = data.ss || "";
            $scope.att.categories = data.cat || "";
            updatePager(data.start, data.count, data.n_attendees)
          });
        },
        function(ro){
          $log.error('getAttendees', ro);
        }
      );
      return q.promise;
    },
    getAttendee: function(id){
      var q = $q.defer();
      api('getAttendee', {id: id}).then(
        function(data){
          $log.info('gotAttendee', data);
          $timeout(function() {
            $scope.attendee = data.attendee;
            $scope.bdate = new Date($scope.attendee.birthdate);
            $scope.pdate = new Date($scope.attendee.paydate ? $scope.attendee.paydate : null)
          });
        },
        function(err){
          $log.error('getAttendee', err);
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
    resendConfirmation: function() {
      var q = $q.defer();
      api('resendConfirmation', {
        id: $scope.attendee.id,
      }).then(
        function(ro){
          $log.info('Confirmation resent');
        },
        function(ro){
          $log.error('resendConfirmation', ro);
          $timeout(function() {
            q.reject(ro);
          })
        }
      );
      return q.promise;
    },
    updateAttendee: function() {
      var q = $q.defer();
      api('updateAttendee', {
        id: $scope.attendee.id,
        attendee: $scope.attendee,
      }).then(
        function(ro){
          $log.info('Attendee updated');
        },
        function(ro){
          $log.error('getAttendees', ro);
          $timeout(function() {
            q.reject(ro);
          })
        }
      );
      return q.promise;
    },
    uploadPhoto: function(attendee, imagedata){
      api('uploadPhoto', {
        photo: imagedata,
        idsub: attendee.id,
      }).then(
        function(){
          $timeout(function(){
            console.log('upload succeeded');
            initPhoto(attendee);
          })
        },
        function(err){
          $timeout(function(){
            console.error(err);
          });
        }
      );
    }
  };

  function queryParams(){
    return {

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
      attendee_service.getAttendees();
    },
    next: function(){
      if ($scope.pager.start + $scope.pager.count < $scope.pager.total) {
        $scope.pager.start += $scope.pager.count;
        attendee_service.getAttendees();
      }
    },
    prev: function(){
      if ($scope.pager.start > 0) {
        $scope.pager.start -= $scope.pager.count;
        if ($scope.pager.start < 0) $scope.pager.start = 0;
        attendee_service.getAttendees();
      }
    }
  };

  $scope.photourl = function(p){
    return '/api/photo/' + ((p && p.id) ? p.id : 0);
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
          $scope.attendee.first_name + "?")) {
        attendee_service.deleteAttendee().then(initAttendees);
      }
    },
    cancel: function(){
      this.status = '';
      $scope.tab = tabs.attendees
    },
    open_add: function(){
      this.status = 'add';
      $scope.tab = tabs['detail'];
      $scope.detailmode = 'new';
      angular.extend($scope.attendee,{
        last_name: '',
        first_name: '',
        chesstitle: '',
        category: 'EAT',
        gender: 'M',
        meals: ''
      });
    },
    open_edit: function(p){
      $scope.detailmode = 'edit';
      $scope.tab = tabs['detail'];
      attendee_service.getAttendee(p.id);
    },
    open_photo: function(p){
      initPhoto(p);
    },
    resend_confirmation: function(){
      attendee_service.resendConfirmation().then(
        function(data){
          alert('Confirmation for attendee ' + data.idbel + ' resent');
          $scope.att.status = 'editsaved';
          $log.info('categories', $scope.att.cat);
          attendee_service.getAttendees();
        },
        function(ro) {
          alert(ro);
        }
      )
    },
    save_add: function(){
      attendee_service.addAttendee().then(
        function(data){
          alert('Attendee saved with id: ' + data.idbel);
          $scope.att.status = 'addsaved';
          $scope.attendee.idbel = data.idbel;
        },
        function(ro) {
          alert(ro);
        }
      )
    },
    save_edit: function(){
      attendee_service.updateAttendee().then(
        function(data){
          alert('Attendee ' + data.idbel + ' updated');
          $scope.att.status = 'editsaved';
          $log.info('categories', $scope.att.cat);
          attendee_service.getAttendees();
        },
        function(ro) {
          alert(ro);
        }
      )
    },
    search: function(){
        attendee_service.getAttendees();
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
    printall: attendee_service.printallbadges,
    printselected: function(){
      var ids = [];
      $scope.badges.forEach(function(v,ix) {
        ids.push(v.id_national);
      });
      attendee_service.printbadges(ids);
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
    printall: attendee_service.printallnamecards,
    printselected: function(){
      var ids = [];
      $scope.cards.forEach(function(v,ix) {
        ids.push(v.id_national);
      });
      attendee_service.printnamecards(ids);
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
      attendee_service.uploadPhoto($scope.attendee,
          $scope.photo.cropresult);

    }
  };

  $scope.$watch('photo.data', function () {
    var reader;
    console.log('watched');
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
    $scope.tab = tabs.overview;
    $scope.att.status = '';
    attendee_service.getAttendees();
  }

  function initPhoto(p){
    $scope.attendee = {};
    console.log('going to tab', tabs.photo);
    $scope.tab = tabs.photo;
    randomstr = Math.ceil(Math.random()*10000);
    attendee_service.getAttendee(p.id);
    $scope.photo.init()
  }

  initAttendees();

});

