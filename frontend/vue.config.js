// vue.config.js

const BundleTracker  = require('webpack-bundle-tracker');

module.exports = {
  configureWebpack: {
    plugins: [
      new BundleTracker({
        indent: 2,
        // publicPath: process.env.NODE_ENV === 'production' ? '/static/' : 'http://192.168.0.140:8080/static/'
        publicPath: process.env.NODE_ENV === 'production' ? '/static/' : 'http://localhost:8080/static/'
      })
    ]
  },
  outputDir: 'dist/static',
  baseUrl: "/static",
  crossorigin: "anonymous",
  runtimeCompiler: true,
  pages: {
    cms: 'src/cms.js',
    adm: 'src/adm.js',
    tournament: 'src/tournament.js',
  }
}
  