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
    landingspage:  {
      entry: 'src/pages/landingspage.js',
      filename: (process.env.NODE_ENV == 'development') ?  'dist/landingspage.html' : '../../templates/landingspage.html',
    },
    default:  {
      entry: 'src/pages/default.js',
      filename: (process.env.NODE_ENV == 'development') ?  'dist/default.html' : '../../templates/default.html',
    }
  },
  outputDir: '../backend/bycco/static/fe',
  publicPath: '/static/fe'
}