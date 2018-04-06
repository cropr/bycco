import schemas from './apidef';
import axios from 'axios';
import _ from 'lodash';

axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = 'csrftoken';

export default function(name, params) {

  let schema, surl, options, _body = undefined,
      body = {}, sbody,
      headers = {}, sheaders,
      query= {}, squery,
      path= {}, spath,
      all = {};

  console.log('api call', name, params);
  schema = schemas[name];
  if (!schema) {
    console.error('schema not found:', name );
    return Promise.reject(new Error('schama ' + name + ' not found'))
  }

  // check required paramaters
  if (schema.required) {
    if (!schema.required.every(function(k){
      return k in params;
    })) {
      console.log('api call', name, 'failed: missing_param', all);
      return $q.reject(new Error('missing_param'));
    }
  }

  // fill in all parameters
  sbody = schema.body || [];
  sheaders = schema.headers || [];
  squery = schema.query || [];
  spath = schema.path || [];
  _.forEach(params, function(v, k){
    if (k == '_body') {
      _body = v;
      return;
    }
    if (sbody.indexOf(k) !== -1) {
      all[k] = true;
      body[k] = v;
      return;
    }
    if (sheaders.indexOf(k) !== -1) {
      all[k] = true;
      headers[k] = v;
      return
    }
    if (squery.indexOf(k) !== -1) {
      all[k] = true;
      query[k] = v;
      return;
    }
    if (spath.indexOf(k) !== -1) {
      all[k] = true;
      path[k] = v;
      return;
    }
  });

  // set axios options dict
  surl = schema.url;
  _.forEach(path, function(val, pp){
    surl = surl.replace('{' + pp + '}', val)
  });
  headers['Accept'] = 'application/json';
  headers['Content-Type'] = 'application/json';
  options = {
    method: schema.method,
    url: window.config.apiurl +  surl,
    params: query,
    data: (_body === undefined) ? body : _body,
    headers: headers
  };

  // make http call in a Promise
  return new Promise(function(resolve, reject){
    axios.request(options).then(
      function(data){
        console.log('api call', name, 'successful', data);
        resolve(data.data);
      },
      function(data){
        console.log('api call', name, 'failed', data);
        reject(data);
      }
    )
  });

}
