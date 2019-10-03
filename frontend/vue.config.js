// vue.config.js

const BundleTracker  = require('webpack-bundle-tracker');

module.exports = {
  configureWebpack: {
    plugins: [
      new BundleTracker({
        indent: 2,
        publicPath: process.env.NODE_ENV === 'production' ? '/static/' : 
          'http://localhost:8080/static/',
      })
    ],
    devServer: {
      publicPath: '/static',
      port: 8080,
    }      
  },
  outputDir: 'dist/static',
  publicPath: "/static/",
  crossorigin: "anonymous",
  runtimeCompiler: true,
  pages: {
    cms: {
      entry: 'src/cms.js',
      filename: 'cms.html',
      // chunks: ['chunk-vendors',  'cms'],
    },
    mgmt: {
      entry: 'src/mgmttournament.js',
      filename: 'mgmttournament.html',
      // chunks: ['chunk-vendors',  'mgmttournament'],
    },
    tournament: {
      entry: 'src/tournament.js',
      filename: 'tournament.html',
      // chunks: ['chunk-vendors',  'tournament'],
    }
  }
}
  