'use strict';

angular.module('subscription', [
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

.controller('subCtrl', function($scope, $http, $q, $log){

  var subscription = {
    confirm: function() {
      var q = $q.defer();
      $http.post('/cd_subscription/api/subscription/' + subscription.id + '/confirmation').then(
        (function(ro){
          this.confirmed = true;
          q.resolve(ro.data)
        }).bind(this),
        function(ro){
          q.reject(ro.status);
        }
      );
      return q.promise;
    },
    init: function(obj){
      if (obj) angular.extend(this, obj);
      this.posted = false;
      this.confirmed = false;
      this.photouploaded = false;
    },
    searchIdFide: function(id_fide){
      var q = $q.defer();
      $http.get('/cd_subscription/api/fideplayer/' + id_fide + '/').then(
        function(ro){
          q.resolve(ro.data)
        },
        function(ro){
          q.reject(ro.status);
        }
      );
      return q.promise;
    },
    searchIdNational: function(id_national) {
      var q = $q.defer();
      $http.get('/cd_subscription/api/belplayer/' + id_national + '/').then(
        function(ro){
          q.resolve(ro.data)
        },
        function(ro){
          q.reject(ro.status);
        }
      );
      return q.promise;
    },
    subscribe: function() {
      if (this.id) {
        return this.updatesubscription();
      }
      var q = $q.defer();
      $http.post('/cd_subscription/api/subscription', this).then(
        (function(ro){
          q.resolve(ro.data);
          this.posted = true;
          this.id = ro.data.id;
        }).bind(this),
        function(ro){
          q.reject(ro.status);
        }
      );
      return q.promise;
    },
    updatesubscription: function(){
      var q = $q.defer();
      $http.put('/cd_subscription/api/subscription/' + this.id, this).then(
        (function(ro){
          q.resolve(ro.data);
        }).bind(this),
        function(ro){
          q.reject(ro.status);
        }
      );
      return q.promise;
    },
    uploadPhoto: function(imagedata){
      var q = $q.defer();
      $http.post('/cd_subscription/api/subscription/' + subscription.id + '/photo',
            {imagedata: imagedata}).then(
        (function(ro){
          q.resolve(ro.data);
          this.photouploaded = true;
        }).bind(this),
        function(ro){
          q.reject(ro.status);
        }
      );
      return q.promise;
    }
  };

  function invalidField(field) {
    if (!field) return true;
    return field.length < 2;
  }

  $scope.photo = {
    prupload: {},
    data: "",
    cropsource: "",
    cropsresult: {},
    init: function(){
      this.prupload = {};
      this.data = "";
      this.cropsource = "";
      this.cropsresult = {};
    }
  };

  $scope.$watch('photo.data', function () {
    var reader;
    $log.debug('file:', $scope.photo.data);
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

  $scope.optyears = {};

  $scope.sub = {
    adult: false,
    confirmationfailed: false,
    id_national: '',
    max_tabix: 0,
    searched: false,
    subscriptionconfirmed: false,
    tabix: 0,
    birthdate: function() {
      return (this.day<10? '0': '') + this.day + '/' +
          (this.month <10? '0': '') + this.month  + '/' + this.year;
    },
    checkIdNational: function(){
      this.searched = true;
      subscription.searchIdNational(this.id_national).then(
        (function (player){
          if (player.alreadysubscribed) {
            this.clearPlayer(497);
            return;
          }
          this.setPlayer(player);
          if (player.id_fide && player.id_fide.length) {
            subscription.searchIdFide(player.id_fide).then(
              this.setFidePlayer.bind(this),
              this.clearFidePlayer.bind(this)
            )
          }
        }).bind(this),
        this.clearPlayer.bind(this)
      );
    },
    checkDetails: function(){
      var requiredmissing = false;
      if (!this.adult) {
        if (invalidField(this.fullnameparent)) requiredmissing = true;
        if (invalidField(this.emailparent)) requiredmissing = true;
        if (invalidField(this.mobileparent)) requiredmissing = true;
        if (!$scope.parentispresent) {
          if (invalidField(this.fullnameattendant)) requiredmissing = true;
          if (invalidField(this.mobileattendant)) requiredmissing = true;
        }
      }
      else {
        if (invalidField(this.emailplayer)) requiredmissing = true;
        if (invalidField(this.mobileplayer)) requiredmissing = true;
      }
      if (requiredmissing) {
        console.log('required missing');
        $scope.requiredmissing = true;
        return;
      }
      subscription.init({
        category: (this.belplayer.gender == 'M' ? 'B' : 'G') + this.category,
        emailparent: this.emailparent || '',
        emailplayer: this.emailplayer || '',
        fullnameattendant: this.fullnameattendant || '',
        fullnameparent: this.fullnameparent || '',
        id_national: this.id_national,
        mobileattendant: this.mobileattendant || '',
        mobileparent: this.mobileparent || ''
      });
      subscription.subscribe().then(
        (function(data) {
          this.error403 = false;
          this.paymessage = data.paymessage;
          this.gotoTab(3);
        }).bind(this),
        (function(data) {
          console.error('subscription failed', data);
          if (data == 403) {
            this.error403 = true;
          }
        }).bind(this)
      );
    },
    clearFidePlayer: function(status){
      this.fideplayer = null;
      this.natstatus = 'maybe';
    },
    clearPlayer: function(status){
      this.name = null;
      this.firstname = null;
      this.belplayer = null;
      this.found = false;
      $scope.photo.init();
      switch (status){
        case 0:
        case 404:
        case 497:
        case 498:
        case 499:
          this.errorbelplayer = status;
          break;
        default:
          this.errorbelplayer = 498;
      }
    },
    confirm: function(){
      subscription.confirm().then(
        function(){
          console.log('sub confirmed', this);
          this.subscriptionconfirmed = true;
        }.bind(this),
        function(){
          this.confirmationfailed = true;
        }.bind(this)
      );
    },
    fullname: function(){
      return this.firstname + ' ' + this.name;
    },
    gotoTab: function(ix) {
      this.tabix = ix;
      this.max_tabix = Math.max(this.max_tabix, ix);
    },
    newsubscription: function() {
      location.reload();
    },
    setFidePlayer: function(player) {
      this.fideplayer = player;
      if (player.fidenation == 'BEL') {
          this.natstatus = 'fidebelg';
      }
      else {
        this.natstatus = 'nobelg';
      }
    },
    setPlayer: function(player) {
      var rs = [],
          self = this,
          cat = [
            {cat: 20, label: '-20', year: 1997},
            {cat: 18, label: '-18', year: 1999},
            {cat: 16, label: '-16', year: 2001},
            {cat: 14, label: '-14', year: 2003},
            {cat: 12, label: '-12', year: 2005},
            {cat: 10, label: '-10', year: 2007},
            {cat: 8, label: '--8', year: 2009}
          ];
      this.name = player.name;
      this.firstname = player.firstname;
      this.belplayer = player;
      this.found = true;
      this.errorbelplayer = 0;
      this.year = Number(player.birthdate.substr(0,4));
      this.month = Number(player.birthdate.substr(5,2));
      this.day = Number(player.birthdate.substr(8,2));
      this.adult = new Date(this.year, this.month-1,this.day) < new Date(1999,3,9);
      cat.forEach(function(v){
        if (v.year <= self.year) {
          rs.push({label: v.label, value: v.cat});
          self.category = v.cat;
        }
      });
      $scope.optyears = rs;
    },
    uploadPhoto: function(){
      if (!$scope.photo.cropresult || !$scope.photo.cropresult.length) {
        this.gotoTab(4);
        return;
      }
      subscription.uploadPhoto($scope.photo.cropresult).then(
          (function(){
            console.log('upload succeeded');
            this.gotoTab(4)
          }).bind(this)
      );
    }
  }

});


