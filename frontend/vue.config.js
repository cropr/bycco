module.exports = {
  "transpileDependencies": [
    "vuetify"
  ],
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
      },   
      '/static': {
        target: 'http://localhost:5000',
      }     
    }
  },
  pages: {
    default:  {
      entry: 'src/pages/default.js',
      filename: (process.env.NODE_ENV == 'development') ?  'dist/default.html' : '../../templates/default.html',
    },
    landingspage:  {
      entry: 'src/pages/landingspage.js',
      filename: (process.env.NODE_ENV == 'development') ?  'dist/landingspage.html' : '../../templates/landingspage.html',
    },
    mgmt:  {
      entry: 'src/mgmt/mgmt.js',
      filename: (process.env.NODE_ENV == 'development') ?  'dist/mgmt.html' : '../../templates/mgmt.html',
    },
  },
  outputDir: '../backend/bycco/static/fe',
  publicPath: '/static/fe'
}