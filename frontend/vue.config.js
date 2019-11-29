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
    page:  {
      entry: 'src/pages/page.js',
      filename: (process.env.NODE_ENV == 'development') ?  'dist/page.html' : '../../templates/page.html',
    },
    mgmt:  {
      entry: 'src/mgmt/mgmt.js',
      filename: (process.env.NODE_ENV == 'development') ?  'dist/mgmt.html' : '../../templates/mgmt.html',
    },
  },
  outputDir: '../backend/bycco/static/fe',
  publicPath: '/static/fe'
}