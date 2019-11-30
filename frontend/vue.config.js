
console.log('filenamedir', process.env.VUE_APP_FILENAMEDIR)

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
      entry: 'src/user/page.js',
      filename: process.env.VUE_APP_FILENAMEDIR + 'page.html',
    },
    mgmt:  {
      entry: 'src/mgmt/mgmt.js',
      filename: process.env.VUE_APP_FILENAMEDIR + 'mgmt.html',
    },
    // subscription:  {
    //   entry: 'src//user/subscription.js',
    //   filename: process.env.VUE_APP_FILENAMEDIR + 'subscription.html',
    // },
  },
  outputDir: '../backend/bycco/static/fe',
  publicPath: '/static/fe'
}