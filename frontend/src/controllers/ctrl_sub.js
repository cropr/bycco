angular.module('subscription', [
  'ngAnimate',
  'ngAria',
  'ngFileUpload',
  'ngImgCrop',
  'ngMaterial',
  'ngSanitize'
])

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
    searchIdFide: function(idfide){
      var q = $q.defer();
      $http.get('/api/subscription/fideplayer/' + idfide).then(
        function(ro){
          q.resolve(ro.data)
        },
        function(ro){
          q.reject(ro.status);
        }
      );
      return q.promise;
    },
    searchIdNational: function(idbel) {
      var q = $q.defer();
      $http.get('/api/subscription/belplayer/' + idbel).then(
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
      $http.post('/api/subscription/subscriptions', this).then(
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
    birthdateformat: function() {
      return (this.day<10? '0': '') + this.day + '/' +
          (this.month <10? '0': '') + this.month  + '/' + this.year;
    },
    checkIdNational: function(){
      this.searched = true;
      subscription.searchIdNational(this.idbel).then(
        (function (player){
          if (player.alreadysubscribed) {
            this.clearPlayer(497);
            return;
          }
          this.setPlayer(player);
          if (player.idfide && player.idfide.length) {
            subscription.searchIdFide(player.idfide).then(
              this.setFidePlayer.bind(this), null
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
        category: (this.gender == 'M' ? 'B' : 'G') + this.category,
        emailparent: this.emailparent || '',
        emailplayer: this.emailplayer || '',
        fullnameattendant: this.fullnameattendant || '',
        fullnameparent: this.fullnameparent || '',
        idbel: this.idbel,
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
    clearPlayer: function(status){
      this.init();
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
      return this.first_name + ' ' + this.last_name;
    },
    gotoTab: function(ix) {
      this.tabix = ix;
      this.max_tabix = Math.max(this.max_tabix, ix);
    },
    init: function(){
      this.adult =  false;
      this.confirmationfailed = false;
      this.idbel =  null;
      this.max_tabix = 0;
      this.searched = false;
      this.subscriptionconfirmed =  false;
      this.tabix =  0;
      this.fideplayer = null;
      this.currentratingbel = 0;
      this.currentratingfide = 0;
      $scope.photo.init();
    },
    newsubscription: function() {
      location.reload();
    },
    setFidePlayer: function(player) {
      this.ratingsfide = player.ratingsfide;
      this.nationalityfide = player.nationalityfide;
      this.chesstitle = player.chesstitle;
      this.currentratingfide = player.currentrating;
    },
    setPlayer: function(player) {
      var rs = [],
          self = this,
          cat = [
            {cat: 20, label: '-20', year: 1998},
            {cat: 18, label: '-18', year: 2000},
            {cat: 16, label: '-16', year: 2002},
            {cat: 14, label: '-14', year: 2004},
            {cat: 12, label: '-12', year: 2006},
            {cat: 10, label: '-10', year: 2008},
            {cat: 8, label: '--8', year: 2010}
          ];
      this.last_name = player.last_name;
      this.first_name = player.first_name;
      this.gender = player.gender;
      this.ratingsbel = player.ratingsbel;
      this.currentratingbel = player.currentrating;
      this.nationalitybel = player.nationalitybel;
      this.birthdate = player.birthdate;
      this.idbel = player._id;
      this.idfide = player.idfide;
      this.found = true;
      this.errorbelplayer = 0;
      this.year = Number(player.birthdate.substr(0,4));
      this.month = Number(player.birthdate.substr(5,2));
      this.day = Number(player.birthdate.substr(8,2));
      this.adult = new Date(this.year, this.month-1,this.day) < new Date(2000,3,8);
      cat.forEach(function(v){
        if (v.year <= self.year) {
          rs.push({label: v.label, value: v.cat});
          self.category = v.cat;
        }
      });
      console.log('sub after setPlayer', this);
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
  };

  $scope.sub.init();

});
