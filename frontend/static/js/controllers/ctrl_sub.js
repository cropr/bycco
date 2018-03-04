angular.module('subscription', [
  'ngAnimate',
  'ngAria',
  'ngFileUpload',
  'ngMaterial',
  'ngSanitize',
  'uiCropper',
  'common',
])

.controller('subCtrl', function($scope, $http, $q, $log, $timeout, api){

  let subparam = {};

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
      var self=this;
      this.searched = true;
      this.errorcode = null;
      api('searchIdNational', {idbel: this.idbel}).then(
        function (player){
          $timeout(function(){
            console.log('success ', player, self);
            if (player.alreadysubscribed) {
              self.errorcode = 'alreadyregistered';
              self.found = false;
              return;
            }
            let db = new Date(player.birthdate);
            if (db.getFullYear() < 1998) {
              self.errorcode = 'playeradult';
              self.found = false;
              return;
            }
            self.setPlayer(player);
            if (player.idfide && player.idfide.length) {
              api('searchIdFide', {idfide:player.idfide}).then(
                function(player){
                  $timeout(self.setFidePlayer.bind(self)(player));
                },
                null
              )
            }
          })
        },
        function(err){
          $timeout(function(){
            console.error('Could not get id national', err, self);
            if (err.status == 404) {
              self.errorcode = 'notfound';
              self.found = false;
              return
            }
            self.errorcode = 'unknown';
          })
        }
      );
    },
    createSubscription: function(){
      var rm = false, self=this;
      if (!this.adult) {
        rm = rm || invalidField(this.fullnameparent);
        rm = rm || invalidField(this.emailparent);
        rm = rm || invalidField(this.mobileparent);
        if (!$scope.parentispresent) {
          rm = rm || invalidField(this.fullnameattendant);
          rm = rm || invalidField(this.mobileattendant);
        }
      }
      else {
        rm = rm || invalidField(this.emailplayer);
        rm = rm || invalidField(this.mobileplayer);
      }
      if (rm) {
        this.errorcode = 'invalidfield';
        return;
      }
      this.setSubparam();
      api('createSubscription', {subscription: subparam}).then(
        function(data) {
          $timeout(function(){
            self.paymessage = data.paymessage;
            self.idsub = data.id;
            self.gotoTab(3);
          });
        },
        function(data) {
          $timeout(function(){
            console.error('subscription failed', data);
            self.errorcode = (data == 403) ? 'firewall' : 'unknown';
          })
        }
      );
    },
    clearPlayer: function(){
      this.found = false;
      this.errorcode = null;
      this.confirmationfailed = false;
      this.idbel =  null;
      this.subscriptionconfirmed =  false;
      this.fideplayer = null;
      this.currentratingbel = 0;
      this.currentratingfide = 0;
      this.adult =  false;
      this.emailplayer = '';
      this.mobileplayer = '';
      this.fullnameparent = '';
      this.emailparent = '';
      this.mobileparent = '';
      this.fullnameattendant = '';
      this.mobilemobileattendant = '';
      this.firewall = false;
      this.privacy = false;
      this.nationagree = false;
      subparam = {};
    },
    confirm: function(){
      var self=this;
      this.errorcode = null;
      api('confirmSubscription',{
        idsub: this.idsub
      }).then(
        function(){
          $timeout(function(){
            console.log('sub confirmed', self);
            self.subscriptionconfirmed = true;
          })
        },
        function(){
          $timeout(function() {
            self.confirmationfailed = true;
          })
        }
      );
    },
    fullname: function(){
      return this.first_name + ' ' + this.last_name;
    },
    gotoTab: function(ix) {
      this.tabix = ix;
      this.max_tabix = Math.max(this.max_tabix, ix);
      this.errorcode = null;
    },
    init: function(){
      this.max_tabix = 0;
      this.subscriptionconfirmed =  false;
      this.tabix =  0;
      this.clearPlayer();
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
      this.natstatus =  (player.nationalityfide == 'BEL') ? 'fidebelg': 'nobelg';
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
      this.idclub = player.idclub;
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
      this.natstatus = 'maybe';
      console.log('sub after setPlayer', this);
      $scope.optyears = rs;
    },
    setSubparam: function(){
      subparam =  {
        category: (this.gender == 'M' ? 'B' : 'G') + this.category,
        emailparent: this.emailparent || '',
        emailplayer: this.emailplayer || '',
        fullnameattendant: this.fullnameattendant || '',
        fullnameparent: this.fullnameparent || '',
        idbel: this.idbel,
        mobileattendant: this.mobileattendant || '',
        mobileparent: this.mobileparent || '',
        paymessage: this.paymessage,
      };
    },
    uploadPhoto: function(){
      var self=this;
      this.errorcode = null;
      if (!$scope.photo.cropresult || !$scope.photo.cropresult.length) {
        this.gotoTab(4);
        return;
      }
      api('uploadPhoto', {
        photo: $scope.photo.cropresult,
        idsub: this.idsub,
      }).then(
        function(){
          $timeout(function(){
            console.log('upload succeeded');
            self.gotoTab(4)
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

  $scope.sub.init();

});
