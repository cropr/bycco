// vue.config.js

const BundleTracker  = require('webpack-bundle-tracker');

module.exports = {
  configureWebpack: {
    plugins: [
      new BundleTracker({
        indent: 2,
        publicPath: 'http://localhost:8080/static/'
      })
    ]
  },
  outputDir: '../fe_dist/static',
  baseUrl: "/static",
  crossorigin: "anonymous",
  runtimeCompiler: true,
  pages: {
    cms: 'src/cms.js',
    adm: 'src/adm.js',
    subscribe: 'src/subscribe.js',
  }
}
  