
module.exports = {
  "transpileDependencies": [
    "vuetify"
  ],
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
      },   
      "/openapi.json": {
        "target": "http://localhost:8000"
      }   
    }
  },
  pages: {
    mgmt:  {
      entry: 'src/mgmt/index.js',
    },
    page:  {
      entry: 'src/page/index.js',
    },
    // participants:  {
    //   entry: 'src/user/participants.js',
    //   filename: process.env.VUE_APP_FILENAMEDIR + 'participants.html',
    // },
    // subscription:  {
    //   entry: 'src/user/subscription.js',
    //   filename: process.env.VUE_APP_FILENAMEDIR + 'subscription.html',
    // },
  },
}