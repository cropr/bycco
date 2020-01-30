
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
    mgmt:  {
      entry: 'src/mgmt/mgmt.js',
      filename: process.env.VUE_APP_FILENAMEDIR + 'mgmt.html',
    },
    page:  {
      entry: 'src/user/page.js',
      filename: process.env.VUE_APP_FILENAMEDIR + 'page.html',
    },
    participants:  {
      entry: 'src/user/participants.js',
      filename: process.env.VUE_APP_FILENAMEDIR + 'participants.html',
    },
    subscription:  {
      entry: 'src/user/subscription.js',
      filename: process.env.VUE_APP_FILENAMEDIR + 'subscription.html',
    },
  },
  outputDir: '../backend/bycco/static/fe',
  publicPath: '/static/fe'
}