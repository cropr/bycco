'use strict';

angular.module('api',[])

.config(function($httpProvider){
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
})

.factory('api',
  function($http, $q, apischema){
    return function(name, params) {

      let apidef, surl, deferred, options, _body = undefined,
          body = {},
          headers = {},
          query= {},
          path= {},
          all = {},
          schema = apischema.schema,
          base_url = apischema.base_url;


      console.log('apicall', name, params);

      if (!(name in schema)) {
        console.log('apicall', name, 'failed: api name unknown');
        return $q.reject(new Error('unknown_api_name'))
      }
      apidef = schema[name];
      apidef.body = apidef.body || [];
      apidef.headers = apidef.headers || [];
      apidef.query = apidef.query || [];
      apidef.path = apidef.path || [];

      // fill in all parameters
      angular.forEach(params, function(v, k){
        if (k == '_body') {
          _body = v;
          return;
        }
        if (apidef.body.indexOf(k) !== -1) {
          body[k] = v;
          all[k] = true;
          return;
        }
        if (apidef.headers.indexOf(k) !== -1) {
          headers[k] = v;
          all[k] = true;
          return
        }
        if (apidef.query.indexOf(k) !== -1) {
          query[k] = v;
          all[k] = true;
          return;
        }
        if (apidef.path.indexOf(k) !== -1) {
          path[k] = v;
          all[k] = true;
          return;
        }
      });

      // check required paramaters
      if (apidef.required) {
        if (!apidef.required.every(function(k){
          return k in all;
        })) {
          console.log('apicall', name, 'failed: missing_param');
          return $q.reject(new Error('missing_param'));
        }
      }
      headers['Accept'] = ['application/json'];
      headers['Content-Type'] = ['application/json'];

      // replace path parameters
      surl = apidef.url;
      angular.forEach(path, function(val, pp){
        surl = surl.replace('{' + pp + '}', val)
      });

      // make http call
      options = {
        method: apidef.method,
        url: base_url +  surl,
        params: query,
        data: (_body === undefined) ? body : _body,
        headers: headers
      };
      deferred = $q.defer();
      $http(options).then(
        function(data){
          console.log('apicall', name, 'successful', data);
          deferred.resolve(data.data);
        },
        function(data){
          console.log('apicall', name, 'failed', data);
          deferred.reject(data);
        }
      );
      return deferred.promise;

    }

  }
)

;
