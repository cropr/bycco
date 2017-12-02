'use strict';


angular.module('cdp_subscribesms', [
  'ngAnimate',
  'ngAria',
  'ngMaterial',
  'ngSanitize'
])

.config(function($httpProvider){
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
})


.controller('subscribeCtrl',
  function($scope, $q, $timeout, $log, $http) {

    var codes = ["31", "32", "33", "352", "49"];


    function subscribe(mobile, id_national){
      var q = $q.defer();
      $http.post('/cd_subscription/api/registersms', {
          mobile: mobile,
          id_national: id_national
        }
      ).then(
        function(data) {
          q.resolve(data)
        },
        function(ro) {
          $log.error('Error from Rest', ro);
          q.reject(ro);
        }
      );
      return q.promise;
    }

    function checknumber(mobile) {
      var err = 1;
      $log.info("checknumber", mobile);
      codes.forEach(function(v) {
        if (mobile.startsWith(v)) {
          err = 0;
        }
      });
      $log.info("starting OK", err);
      if (err == 1) return 1;
      return /^\d{8,}$/.test(mobile) ? 0 : 2;
    }

    $scope.sms = {
      errorcode: 0,
      id_national: "",
      mobile:"",
      sent: false,
      subscribe: function(){
        this.errorcode = checknumber(this.mobile);
        $log.info("errocode", this.errorcode);
        if (this.errorcode > 0) {
          this.sent = true;
          $log.error("Error code", this.errorcode);
          return;
        }
        subscribe(this.mobile, this.id_national).then(
            function(data){
              $scope.sms.fullname = data.fullname;
              this.sent = true;
            }.bind(this),
            function(data){
              this.sent = true;
              if (data.status == 409) {
                this.errorcode = 4;
                $log.info("error 409", $scope.sms)
              }
              if (data.status == 412) {
                this.errorcode = 3;
                $log.info("error 409", $scope.sms)
              }
            }.bind(this)
        )
      }
    };



  }
);
