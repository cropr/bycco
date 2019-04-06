// vue.config.js

const BundleTracker  = require('webpack-bundle-tracker');

module.exports = {
  configureWebpack: {
    plugins: [
      new BundleTracker({
        indent: 2,
        publicPath: process.env.NODE_ENV === 'production' ? '/static/' : 'http://localhost:8080/static/',
        path: process.env.NODE_ENV === 'production' ? '.' : '../build/static/'
      })
    ]
  },
  outputDir: 'dist/static',
  baseUrl: "/static",
  crossorigin: "anonymous",
  runtimeCompiler: true,
  pages: {
    cms: 'src/cms.js',
    mgmttournament: 'src/mgmttournament.js',
    tournament: 'src/tournament.js',
  }
}
  