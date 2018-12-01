'use strict';

console.log('bridge:', window.bridge);

angular.module('common', [])

.factory('bridge', ['$location', function($location){

  window.bridge.gotoAngularRoute = function($path){
    console.log('Going to angular route via bridge', path);
    $location.path(path);
  };
  return {
    updateMenu: window.bridge.updateMenu,
  }
}])

.factory('api', function(){
    return window.bridge.api
  }
)

;

